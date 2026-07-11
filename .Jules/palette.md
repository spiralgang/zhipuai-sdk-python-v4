## 2025-05-22 - Improved SDK Error Traceability
**Learning:** For API SDKs, the "user interface" is the error message and debugging information. Providing structured error messages and unique identifiers (like request IDs) directly in the exception string drastically reduces developer friction during troubleshooting.
**Action:** Always check if core error handling logic can be enriched with more context from the API response (JSON messages, headers) without breaking existing exception signatures.
