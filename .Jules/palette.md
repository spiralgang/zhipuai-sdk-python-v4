## 2025-05-14 - Structured API Error Messaging for DX
**Learning:** In a developer-facing SDK, the "User Experience" is primarily the Developer Experience (DX). Generic error messages that dump raw response text force developers to manually parse logs. Providing structured, human-readable error messages with traceability IDs (like request_id) significantly reduces debugging friction.
**Action:** Always look for centralized error handling logic in SDKs and ensure it extracts meaningful messages from API responses, falling back gracefully to raw output if parsing fails.

## 2025-05-15 - Programmatic Access to Traceability IDs
**Learning:** For SDKs, "UI" is the API surface. Adding direct attributes like `.request_id` and `.message` to exception objects provides a much better developer experience than forcing them to parse a formatted error string. It enables automated error logging and reporting tools to work more effectively.
**Action:** When designing or modifying error classes in an SDK, ensure key metadata from the API response is exposed as public attributes on the exception object.

## 2025-05-16 - Safe and Structured Key Format Validation in SDKs
**Learning:** For developer-facing SDKs, custom exceptions raised during early-stage format validation (like API key parsing) provide excellent fast-feedback. However, to prevent accidental exposure of sensitive user input in application logs or tracebacks, validation messages should explain the expected format clearly but must never echo the raw, invalid API key back to the user.
**Action:** Always omit or scrub potentially sensitive raw input when crafting client-side format validation exception messages.
