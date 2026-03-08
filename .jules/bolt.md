## 2025-05-15 - [Guarding expensive logging arguments]
**Learning:** Accessing `requests.Response.text` triggers automatic decoding of the response content, which can be expensive for large payloads. In Python's `logging` module, arguments passed to logging methods are evaluated even if the message is not emitted due to the current log level.
**Action:** Always wrap logging calls that access `response.text` or perform other expensive operations in an `if logger.isEnabledFor(LEVEL)` block.
