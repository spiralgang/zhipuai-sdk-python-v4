## 2025-05-14 - Improved API Error Clarity
**Learning:** For API SDKs, the "user interface" includes error messages. Providing structured messages that extract specific details (like 'message' or 'msg') from JSON error responses and including trace IDs (like 'x-request-id') significantly improves the developer experience and speed of debugging.
**Action:** Always check if error responses contain JSON with descriptive messages and ensure that relevant headers for tracing are included in the exception message.
