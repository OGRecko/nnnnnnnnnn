# Directivity parser fixtures

`valid-*` files are SYNTHETIC patterns used only to exercise the parser. They are not measurements of any real speaker and must never be shipped as speaker data.

`hostile-*` files are malformed or malicious inputs that `parseDirectivityFile` must reject with a clear error (or, for `hostile-proto-keys.json`, parse without polluting `Object.prototype`).
