/**
 * Structured, redacted logging and a bounded metrics registry.
 *
 * - Metric names come from a FIXED allow-list, so attacker-controlled input can
 *   never create new metric series (bounded cardinality, no memory growth).
 * - Metrics carry no labels at all: no IPs, IDs or tokens can ever enter them.
 * - Log redaction is substring/pattern based and deep, and is also applied to
 *   error text, so a secret embedded in an exception message is scrubbed.
 */

export const METRIC_NAMES = [
  'simulations_started',
  'simulations_completed',
  'simulations_failed',
  'simulations_cancelled',
  'jobs_recovered',
  'duplicate_claims_rejected',
  'rate_limit_rejections',
  'concurrency_rejections',
  'resource_limit_rejections',
  'storage_failures',
  'cleanup_deletions',
  'cleanup_failures',
  'worker_timeouts',
  'auth_rejections',
] as const;
export type MetricName = (typeof METRIC_NAMES)[number];
const ALLOWED = new Set<string>(METRIC_NAMES);

export class Metrics {
  private counters = new Map<string, number>(METRIC_NAMES.map((n) => [n, 0]));
  inc(name: string, by = 1): void {
    if (!ALLOWED.has(name)) return; // unknown names are dropped, never created
    this.counters.set(name, (this.counters.get(name) ?? 0) + by);
  }
  snapshot(): Record<string, number> { return Object.fromEntries(this.counters); }
  reset(): void { for (const k of this.counters.keys()) this.counters.set(k, 0); }
}

export const metrics = new Metrics();
export const incrementMetric = (name: string, by = 1) => metrics.inc(name, by);
export const getMetrics = () => metrics.snapshot();

// --------------------------------------------------------------- redaction

const SENSITIVE_KEY_RE = /(token|authorization|cookie|password|passwd|secret|private.?key|client.?email|service.?account|api.?key|credential|session)/i;

const PATTERNS: Array<[RegExp, string]> = [
  [/Bearer\s+[A-Za-z0-9._~+/=-]+/gi, 'Bearer [REDACTED]'],
  [/-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----/g, '[REDACTED PRIVATE KEY]'],
  [/-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*/g, '[REDACTED PRIVATE KEY]'],
  [/"private_key"\s*:\s*"[^"]*"/gi, '"private_key":"[REDACTED]"'],
  // Anchored to the start of an identifier run: without the lookbehind the engine restarts at every character of a
  // long alphanumeric string and the cost is quadratic (a 100 KB string took ~11 s).
  [/(?<![A-Za-z0-9_.-])([A-Za-z0-9_.-]*(?:token|secret|password|api[_-]?key|authorization)[A-Za-z0-9_.-]*)\s*[=:]\s*("[^"]*"|'[^']*'|[^\s,;&}]+)/gi, '$1=[REDACTED]'],
  // 64-hex strings are capability tokens (or their hashes): never log either.
  [/\b[a-f0-9]{64}\b/gi, '[REDACTED HEX64]'],
  // Google API keys and OAuth-style tokens.
  [/\bAIza[0-9A-Za-z_-]{30,}\b/g, '[REDACTED API KEY]'],
  [/\bya29\.[0-9A-Za-z_-]{20,}\b/g, '[REDACTED OAUTH TOKEN]'],
  // IPv4 addresses (client IPs are personal data and are never logged raw).
  [/\b(?:\d{1,3}\.){3}\d{1,3}\b/g, '[IP]'],
  // IPv6 addresses: full form (8 groups) and "::"-compressed forms. The boundary guards keep ordinary text such as
  // "std::add" or a 12:34:56 clock time from being mangled.
  [/(?<![A-Za-z0-9:.])(?:(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}|(?:[A-Fa-f0-9]{1,4}:){1,7}:(?:[A-Fa-f0-9]{1,4}(?::[A-Fa-f0-9]{1,4}){0,6})?|::(?:[A-Fa-f0-9]{1,4}:){0,6}[A-Fa-f0-9]{1,4})(?![A-Za-z0-9:])/g, '[IP]'],
  // E-mail addresses are personal data.
  [/(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}/g, '[EMAIL]'],
  // OS account names embedded in file paths (Windows, macOS, Linux) -- crash stacks routinely contain them.
  [/([A-Za-z]:[\\/]+Users[\\/]+)[^\\/\s"']+/gi, '$1[USER]'],
  [/(\/(?:Users|home)\/)[^\/\s"']+/g, '$1[USER]'],
];

/** Hard bound on what the redactor will scan, so a hostile multi-megabyte string cannot stall the event loop. */
export const MAX_REDACT_INPUT_CHARS = 50_000;

export function redactString(input: string): string {
  let out = String(input).slice(0, MAX_REDACT_INPUT_CHARS);
  for (const [re, rep] of PATTERNS) out = out.replace(re, rep);
  return out;
}

export function redactValue(value: unknown, depth = 0): unknown {
  if (depth > 6) return '[TRUNCATED]';
  if (typeof value === 'string') return redactString(value).slice(0, 2000);
  if (value instanceof Error) return redactString(value.message).slice(0, 2000);
  if (Array.isArray(value)) return value.slice(0, 50).map((v) => redactValue(v, depth + 1));
  if (value && typeof value === 'object') {
    const out: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(value as Record<string, unknown>).slice(0, 50)) {
      out[k] = SENSITIVE_KEY_RE.test(k) ? '[REDACTED]' : redactValue(v, depth + 1);
    }
    return out;
  }
  return value;
}

export type LogSink = (line: string) => void;
let infoSink: LogSink = (l) => console.log(l);
let errorSink: LogSink = (l) => console.error(l);
/** Test hook: capture emitted log lines to assert nothing sensitive is written. */
export function setLogSinks(info: LogSink, error: LogSink): void { infoSink = info; errorSink = error; }
export function resetLogSinks(): void { infoSink = (l) => console.log(l); errorSink = (l) => console.error(l); }

export function logEvent(event: string, fields: Record<string, unknown> = {}): void {
  infoSink(JSON.stringify({ severity: 'INFO', event, timestamp: new Date().toISOString(), ...(redactValue(fields) as object) }));
}

export function logError(event: string, error: unknown, fields: Record<string, unknown> = {}): void {
  const raw = error instanceof Error ? `${error.name}: ${error.message}` : String(error);
  errorSink(JSON.stringify({
    severity: 'ERROR', event, timestamp: new Date().toISOString(),
    error: redactString(raw).slice(0, 1000),
    ...(redactValue(fields) as object),
  }));
}
