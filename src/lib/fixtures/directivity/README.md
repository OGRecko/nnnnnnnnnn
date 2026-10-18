# Directivity import fixtures

`valid-*` files are SYNTHETIC patterns (absolute SPL around 90 dB so normalization is exercised). They are not measurements of any real speaker and must never be shipped as speaker data.

`hostile-*` files must be rejected with a clear, specific error (or, for `hostile-proto.json`, rejected without polluting `Object.prototype`).
