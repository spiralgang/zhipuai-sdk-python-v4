## 2025-05-14 - Structured API Error Messaging for DX
**Learning:** In a developer-facing SDK, the "User Experience" is primarily the Developer Experience (DX). Generic error messages that dump raw response text force developers to manually parse logs. Providing structured, human-readable error messages with traceability IDs (like request_id) significantly reduces debugging friction.
**Action:** Always look for centralized error handling logic in SDKs and ensure it extracts meaningful messages from API responses, falling back gracefully to raw output if parsing fails.
