## 2025-05-14 - Improved Error Traceability and Clarity in SDK

**Learning:** When building an API SDK, raw error responses are often opaque. Extracting structured error messages (e.g., from 'message' or 'msg' fields) and appending the 'x-request-id' directly to the exception message significantly improves Developer Experience (DX) by making issues immediately actionable and traceable without needing to inspect raw response objects.

**Action:** Always attempt to parse JSON error responses and include a unique Request ID in the exception message if available in the headers. Also, ensure "Missing configuration" errors (like missing API keys) provide direct links to the relevant setup page.
