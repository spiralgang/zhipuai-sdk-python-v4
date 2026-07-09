## 2025-05-14 - Improved API Error Clarity
**Learning:** Developers benefit significantly from specific, actionable error messages. In SDKs, centralizing error parsing to extract nested 'message' fields from JSON responses and including request IDs (like `x-request-id`) in the final exception string drastically improves the debugging experience (DX) and traceability.
**Action:** Always check if the API returns a structured error body (e.g., `{"error": {"message": "..."}}`) and prioritize extracting that over raw response text. Ensure correlation IDs are visible in the primary error output.
