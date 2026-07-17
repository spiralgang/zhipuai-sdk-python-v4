## 2025-05-14 - Structured API Error Messaging for DX
**Learning:** In a developer-facing SDK, the "User Experience" is primarily the Developer Experience (DX). Generic error messages that dump raw response text force developers to manually parse logs. Providing structured, human-readable error messages with traceability IDs (like request_id) significantly reduces debugging friction.
**Action:** Always look for centralized error handling logic in SDKs and ensure it extracts meaningful messages from API responses, falling back gracefully to raw output if parsing fails.

## 2025-05-15 - Programmatic Access to Traceability IDs
**Learning:** For SDKs, "UI" is the API surface. Adding direct attributes like `.request_id` and `.message` to exception objects provides a much better developer experience than forcing them to parse a formatted error string. It enables automated error logging and reporting tools to work more effectively.
**Action:** When designing or modifying error classes in an SDK, ensure key metadata from the API response is exposed as public attributes on the exception object.

## 2026-07-17 - Appending Request URL to Exceptions for Debug Context
**Learning:** When debugging SDK client errors or validation failures, developers need to know exactly which endpoint and URL was requested. Without this context, tracking down which API call caused the exception is tedious, especially when multiple requests are made in sequence. Exposing the request URL directly in the exception message dramatically streamlines troubleshooting.
**Action:** Always append the request URL (in the format `, url: {url}`) to exceptions like connection errors, timeouts, validation errors, and status errors in an SDK to provide immediate, actionable debug context.
