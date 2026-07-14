## 2025-05-14 - Structured API Error Messaging for DX
**Learning:** In a developer-facing SDK, the "User Experience" is primarily the Developer Experience (DX). Generic error messages that dump raw response text force developers to manually parse logs. Providing structured, human-readable error messages with traceability IDs (like request_id) significantly reduces debugging friction.
**Action:** Always look for centralized error handling logic in SDKs and ensure it extracts meaningful messages from API responses, falling back gracefully to raw output if parsing fails.

## 2025-05-15 - Programmatic Access to Traceability IDs
**Learning:** For SDKs, "UI" is the API surface. Adding direct attributes like `.request_id` and `.message` to exception objects provides a much better developer experience than forcing them to parse a formatted error string. It enables automated error logging and reporting tools to work more effectively.
**Action:** When designing or modifying error classes in an SDK, ensure key metadata from the API response is exposed as public attributes on the exception object.

## 2026-07-14 - Contextual Awareness in Network Exceptions
**Learning:** For developers, a "Connection error" or "Request timed out" is frustrating because it lacks context. By automatically including the target URL in the error message, we eliminate a step in the debugging process, making the SDK feel more "helpful" and "aware" of the developer's intent.
**Action:** Always ensure network-level exceptions include the context of the failed request (like URL or method) in their default messages.
