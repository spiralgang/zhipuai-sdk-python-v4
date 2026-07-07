## 2026-07-07 - Improved API Error Clarity
**Learning:** For developer tools like SDKs, "Developer Experience" (DX) is equivalent to UX. Clear error messages that extract meaningful descriptions from JSON responses and include traceability identifiers like `x-request-id` significantly reduce user frustration and debugging time.
**Action:** When working on API clients, always ensure that `raise_for_status` type errors are intercepted and enriched with the actual error payload and request IDs.
