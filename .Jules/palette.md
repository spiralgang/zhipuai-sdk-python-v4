## 2025-05-14 - Structured API Error Messaging for DX
**Learning:** In a developer-facing SDK, the "User Experience" is primarily the Developer Experience (DX). Generic error messages that dump raw response text force developers to manually parse logs. Providing structured, human-readable error messages with traceability IDs (like request_id) significantly reduces debugging friction.
**Action:** Always look for centralized error handling logic in SDKs and ensure it extracts meaningful messages from API responses, falling back gracefully to raw output if parsing fails.

## 2025-05-15 - Programmatic Access to Traceability IDs
**Learning:** For SDKs, "UI" is the API surface. Adding direct attributes like `.request_id` and `.message` to exception objects provides a much better developer experience than forcing them to parse a formatted error string. It enables automated error logging and reporting tools to work more effectively.
**Action:** When designing or modifying error classes in an SDK, ensure key metadata from the API response is exposed as public attributes on the exception object.

## 2025-05-16 - Safe Verification of Custom Exception Messages
**Learning:** While custom exception classes in SDKs can define a `.message` attribute for structured access, relying on it in tests or user code can be fragile or rejected by standard Python linters/reviewers. Standard exception handling and assertions should always fallback to checking `str(error)` to ensure maximum robustness and compatibility with standard Python exception contracts.
**Action:** When testing or handling exceptions, always assert or log using `str(error)` alongside or instead of `.message` to avoid potential attribute errors.
