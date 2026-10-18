// Client error reporter. Kept as an external file (not inline in index.html) because the production/desktop
// CSP is script-src 'self' and blocks inline scripts.
//
// Privacy: reports contain only the error message, the script location and the stack trace, with URL query
// strings and fragments removed. No user content, project data, identifiers or cookies are sent, and the server
// redacts tokens, IP addresses, e-mail addresses and OS account names before logging (server/observability.ts).
// Opt out with the browser's Do Not Track / Global Privacy Control setting, or run in the console:
//   localStorage.setItem('cavity.errorReporting', 'off')
(function () {
  'use strict';
  var MAX_REPORTS_PER_PAGE = 5;
  var sent = 0;
  var seen = Object.create(null);

  function optedOut() {
    try {
      if (navigator.doNotTrack === '1' || window.doNotTrack === '1' || navigator.globalPrivacyControl === true) return true;
    } catch (e) { /* ignore */ }
    try { return window.localStorage.getItem('cavity.errorReporting') === 'off'; } catch (e) { return false; }
  }
  function cut(v, n) { return typeof v === 'string' ? v.slice(0, n) : ''; }
  // Drop ?query and #fragment from every URL in a string.
  function stripUrls(s) { return String(s).replace(/(https?:\/\/[^\s)'"?#]+)[?#][^\s)'"]*/g, '$1'); }
  function ignorable(text) {
    return !text || text === 'Script error.' || text.indexOf('WebSocket') !== -1 || text.indexOf('vite') !== -1;
  }

  function report(message, location, stack) {
    try {
      if (sent >= MAX_REPORTS_PER_PAGE || optedOut()) return;
      message = stripUrls(cut(message, 500));
      if (ignorable(message)) return;
      var key = message + '|' + location;
      if (seen[key]) return;
      seen[key] = true;
      sent++;
      var p = fetch('/api/log-error', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        keepalive: true,
        body: JSON.stringify({ message: message, location: stripUrls(cut(location, 500)), stack: stripUrls(cut(stack, 2000)) })
      });
      // A failed report (offline, blocked, 4xx) must never raise another unhandled rejection: that would re-enter
      // this handler and loop forever.
      if (p && typeof p.catch === 'function') p.catch(function () {});
    } catch (e) { /* the reporter must never throw */ }
  }

  window.addEventListener('error', function (event) {
    try {
      event = event || {};
      var loc = event.filename ? event.filename + ':' + (event.lineno || 0) + ':' + (event.colno || 0) : '';
      report(event.message || (event.error && event.error.message) || '', loc, event.error && event.error.stack ? event.error.stack : '');
    } catch (e) { /* the reporter must never throw */ }
  });
  window.addEventListener('unhandledrejection', function (event) {
    try {
      var r = event && event.reason;
      var msg = r && r.message ? r.message : (r ? String(r) : 'Unhandled Rejection');
      var stack = r && r.stack ? r.stack : '';
      if (ignorable(msg) || (typeof stack === 'string' && stack.indexOf('vite') !== -1)) return;
      report(msg, '', stack);
    } catch (e) { /* the reporter must never throw */ }
  });
})();
