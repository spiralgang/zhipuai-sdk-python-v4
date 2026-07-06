## 2025-05-15 - Enriched Error Messaging for DX
**Learning:** In SDK development, the "UI" is the API and the error messages. Centralizing error parsing to extract human-readable messages from JSON responses and including traceability markers like 'x-request-id' significantly reduces developer frustration and debugging time.
**Action:** Always ensure `HttpClient` error handlers attempt to parse structured error bodies and surface unique request identifiers from headers.
