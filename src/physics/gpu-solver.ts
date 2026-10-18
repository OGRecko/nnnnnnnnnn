
// ---------------------------------------------------------------------------
// GPU compute capability check (WebGL2 / GLSL)
//
// This runs a short, fixed-size benchmark of a wave-equation compute shader
// to check whether the user's browser/GPU supports the floating-point
// texture operations a GPU-accelerated solver would need, and how fast a
// reference workload runs.
//
// IMPORTANT: this does NOT currently accelerate the app's actual room
// simulation. The real FDTD wave solver (RT60/C50/C80/impulse response)
// runs server-side on the CPU (see server.ts). This benchmark is a
// standalone capability/performance check — do not present its timing as
// if it sped up any specific simulation result, and do not report a
// "cores" figure: GPU core counts aren't reliably queryable from the
// browser, and estimating one from navigator.hardwareConcurrency (a CPU
// thread count) would not be a real number.
// ---------------------------------------------------------------------------

const VS_SOURCE = `#version 300 es
in vec2 position;
out vec2 vUv;
void main() {
    vUv = position * 0.5 + 0.5;
    gl_Position = vec4(position, 0.0, 1.0);
}
`;

const FS_SOURCE = `#version 300 es
precision highp float;
precision highp sampler2D;

in vec2 vUv;
out vec4 fragColor;

uniform sampler2D uStatePresent;
uniform sampler2D uStatePast;
uniform float uCourant;
uniform float uDamping;
uniform vec2 uTexelSize;
uniform float uZStride;

void main() {
    // Read present and past pressure
    float pC = texture(uStatePresent, vUv).r;
    float pPast = texture(uStatePast, vUv).r;
    
    // Read 6 immediate neighbors for the 3D Laplacian
    // (Assuming a simplified 2D unwrapping for the benchmark)
    float pL = texture(uStatePresent, vUv - vec2(uTexelSize.x, 0.0)).r;
    float pR = texture(uStatePresent, vUv + vec2(uTexelSize.x, 0.0)).r;
    float pD = texture(uStatePresent, vUv - vec2(0.0, uTexelSize.y)).r;
    float pU = texture(uStatePresent, vUv + vec2(0.0, uTexelSize.y)).r;
    float pB = texture(uStatePresent, vUv - vec2(uZStride, 0.0)).r;
    float pF = texture(uStatePresent, vUv + vec2(uZStride, 0.0)).r;
    
    // The FDTD Wave Equation Core
    float next_p = (2.0 * pC) - pPast + (uCourant * uCourant) * (pL + pR + pU + pD + pF + pB - 6.0 * pC);
    
    // Apply air damping / wall absorption
    next_p *= uDamping;
    
    fragColor = vec4(next_p, 0.0, 0.0, 1.0);
}
`;

function createShader(gl: WebGL2RenderingContext, type: number, source: string) {
    const shader = gl.createShader(type);
    if (!shader) throw new Error("GPU Compile Error: Could not create shader");
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        const info = gl.getShaderInfoLog(shader);
        gl.deleteShader(shader);
        throw new Error("GPU Compile Error: " + info);
    }
    return shader;
}

export interface GPUBenchmarkResult {
    /** Measured wall time for the fixed 10-step reference workload, in ms. 0 when `supported` is false. */
    timeMs: number;
    supported: boolean;
    /** Why the benchmark could not run (only when `supported` is false). Never contains driver paths or stack traces. */
    reason?: string;
}

const BENCHMARK_STEPS = 10;
const unsupported = (reason: string): GPUBenchmarkResult => ({ timeMs: 0, supported: false, reason });

/**
 * Runs the WebGL2 reference workload. NEVER rejects: when WebGL2, float render targets, or enough texture size are
 * unavailable (or anything fails mid-run) it resolves `{ supported: false, reason }`, so the app can fall back to the
 * CPU/server solver without try/catch. All GL objects are released on every path.
 */
export async function runGPUBenchmark(elements: number): Promise<GPUBenchmarkResult> {
    if (!Number.isFinite(elements) || elements < 1 || elements > Number.MAX_SAFE_INTEGER) return unsupported("Invalid element count.");
    if (typeof document === 'undefined' || typeof document.createElement !== 'function') return unsupported("No DOM available (not running in a browser).");

    let gl: WebGL2RenderingContext | null = null;
    const owned: { textures: WebGLTexture[]; framebuffers: WebGLFramebuffer[]; shaders: WebGLShader[]; buffers: WebGLBuffer[]; program: WebGLProgram | null } =
        { textures: [], framebuffers: [], shaders: [], buffers: [], program: null };
    try {
        const canvas = document.createElement('canvas');
        gl = canvas.getContext('webgl2', { antialias: false, preserveDrawingBuffer: false });
        if (!gl) return unsupported("WebGL2 is not supported by this browser/hardware.");
        if (gl.isContextLost()) return unsupported("The WebGL context was lost.");
        // Required for rendering acoustic pressure into float textures.
        if (!gl.getExtension('EXT_color_buffer_float')) return unsupported("EXT_color_buffer_float is not supported; high-precision float render targets are unavailable.");

        // Texture edge for N elements (square packing). The public FDTD ceiling is enforced server-side, not here.
        const texSize = Math.ceil(Math.sqrt(elements));
        const maxTexSize = gl.getParameter(gl.MAX_TEXTURE_SIZE);
        if (!(texSize >= 1) || texSize > maxTexSize) return unsupported(`Texture size ${texSize} exceeds this GPU's limit of ${maxTexSize}.`);
        canvas.width = texSize; canvas.height = texSize;
        gl.viewport(0, 0, texSize, texSize);

        const trackShader = (type: number, src: string) => { const sh = createShader(gl!, type, src); owned.shaders.push(sh); return sh; };
        const vertexShader = trackShader(gl.VERTEX_SHADER, VS_SOURCE);
        const fragmentShader = trackShader(gl.FRAGMENT_SHADER, FS_SOURCE);
        const program = gl.createProgram();
        if (!program) return unsupported("Could not create a WebGL program.");
        owned.program = program;
        gl.attachShader(program, vertexShader); gl.attachShader(program, fragmentShader); gl.linkProgram(program);
        if (!gl.getProgramParameter(program, gl.LINK_STATUS)) return unsupported("GPU shader link failed.");

        const positionBuffer = gl.createBuffer();
        if (!positionBuffer) return unsupported("Could not allocate a vertex buffer.");
        owned.buffers.push(positionBuffer);
        gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW);
        const positionLocation = gl.getAttribLocation(program, "position");
        gl.enableVertexAttribArray(positionLocation);
        gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

        const createTexture = () => {
            const tex = gl!.createTexture();
            if (!tex) throw new Error("Could not allocate a texture.");
            owned.textures.push(tex);
            gl!.bindTexture(gl!.TEXTURE_2D, tex);
            gl!.texImage2D(gl!.TEXTURE_2D, 0, gl!.RGBA32F, texSize, texSize, 0, gl!.RGBA, gl!.FLOAT, null);
            gl!.texParameteri(gl!.TEXTURE_2D, gl!.TEXTURE_MIN_FILTER, gl!.NEAREST);
            gl!.texParameteri(gl!.TEXTURE_2D, gl!.TEXTURE_MAG_FILTER, gl!.NEAREST);
            gl!.texParameteri(gl!.TEXTURE_2D, gl!.TEXTURE_WRAP_S, gl!.CLAMP_TO_EDGE);
            gl!.texParameteri(gl!.TEXTURE_2D, gl!.TEXTURE_WRAP_T, gl!.CLAMP_TO_EDGE);
            return tex;
        };
        let texPresent = createTexture();
        let texPast = createTexture();
        let texFuture = createTexture();
        // Texture allocation can fail asynchronously with OUT_OF_MEMORY on constrained GPUs.
        if (gl.getError() !== gl.NO_ERROR) return unsupported("The GPU could not allocate the benchmark textures.");

        const fbFuture = gl.createFramebuffer();
        if (!fbFuture) return unsupported("Could not allocate a framebuffer.");
        owned.framebuffers.push(fbFuture);
        gl.bindFramebuffer(gl.FRAMEBUFFER, fbFuture);
        gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, texFuture, 0);
        // An incomplete framebuffer silently renders nothing: any timing taken from it would be meaningless.
        if (gl.checkFramebufferStatus(gl.FRAMEBUFFER) !== gl.FRAMEBUFFER_COMPLETE) return unsupported("Float render targets are not usable on this GPU (incomplete framebuffer).");

        gl.useProgram(program);
        gl.uniform1i(gl.getUniformLocation(program, "uStatePresent"), 0);
        gl.uniform1i(gl.getUniformLocation(program, "uStatePast"), 1);
        gl.uniform1f(gl.getUniformLocation(program, "uCourant"), 0.577); // 1/sqrt(3) for 3D stability
        gl.uniform1f(gl.getUniformLocation(program, "uDamping"), 0.999);
        gl.uniform2f(gl.getUniformLocation(program, "uTexelSize"), 1.0 / texSize, 1.0 / texSize);
        // Hardcoded benchmark constant (a ~215^3 cube), NOT a production limit; see the header comment.
        gl.uniform1f(gl.getUniformLocation(program, "uZStride"), 215.0 / texSize);

        const startTime = performance.now();
        for (let i = 0; i < BENCHMARK_STEPS; i++) {
            gl.bindFramebuffer(gl.FRAMEBUFFER, fbFuture);
            gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, texPresent);
            gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, texPast);
            gl.drawArrays(gl.TRIANGLES, 0, 6);
            const tempTex = texPast; texPast = texPresent; texPresent = texFuture; texFuture = tempTex;
            gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, texFuture, 0);
        }
        // Force completion by reading one pixel; otherwise the JS thread continues before the GPU is done.
        gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.FLOAT, new Float32Array(4));
        const endTime = performance.now();

        if (gl.isContextLost()) return unsupported("The WebGL context was lost during the benchmark.");
        const err = gl.getError();
        if (err !== gl.NO_ERROR) return unsupported(`The GPU reported an error during the benchmark (code ${err}).`);

        // Measured time only. No fabricated hardware figures (a real GPU core count is not queryable from a browser).
        return { timeMs: Math.round(endTime - startTime), supported: true };
    } catch (e) {
        // Compile errors and allocation failures land here. The message is reduced to a safe single line.
        const msg = e instanceof Error ? e.message : String(e);
        return unsupported(msg.replace(/\s+/g, ' ').slice(0, 200) || "GPU benchmark failed.");
    } finally {
        // Release GPU memory on EVERY path, including early returns and exceptions.
        if (gl) {
            for (const t of owned.textures) { try { gl.deleteTexture(t); } catch { /* context may be lost */ } }
            for (const f of owned.framebuffers) { try { gl.deleteFramebuffer(f); } catch { /* context may be lost */ } }
            for (const b of owned.buffers) { try { gl.deleteBuffer(b); } catch { /* context may be lost */ } }
            if (owned.program) { try { gl.deleteProgram(owned.program); } catch { /* context may be lost */ } }
            for (const sh of owned.shaders) { try { gl.deleteShader(sh); } catch { /* context may be lost */ } }
        }
    }
}
