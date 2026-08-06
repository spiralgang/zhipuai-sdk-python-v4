## 2025-05-14 - Structured API Error Messaging for DX
**Learning:** In a developer-facing SDK, the "User Experience" is primarily the Developer Experience (DX). Generic error messages that dump raw response text force developers to manually parse logs. Providing structured, human-readable error messages with traceability IDs (like request_id) significantly reduces debugging friction.
**Action:** Always look for centralized error handling logic in SDKs and ensure it extracts meaningful messages from API responses, falling back gracefully to raw output if parsing fails.

## 2025-05-15 - Programmatic Access to Traceability IDs
**Learning:** For SDKs, "UI" is the API surface. Adding direct attributes like `.request_id` and `.message` to exception objects provides a much better developer experience than forcing them to parse a formatted error string. It enables automated error logging and reporting tools to work more effectively.
**Action:** When designing or modifying error classes in an SDK, ensure key metadata from the API response is exposed as public attributes on the exception object.

## 2025-05-16 - Safe Key Verification and Security Leak Prevention
**Learning:** During API key format verification in developer-facing SDKs, raising an exception that echoes invalid or malformed user input can accidentally leak sensitive credentials in application tracebacks or logger outputs. Preventing the echoing of raw inputs is a critical security-centric DX standard.
**Action:** When validating API keys or credentials, raise structured library-specific exceptions detailing the expected format, but strictly avoid printing or echoing any part of the invalid raw input in the exception message.
