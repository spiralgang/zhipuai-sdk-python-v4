from __future__ import annotations

import httpx

__all__ = [
    "ZhipuAIError",
    "APIStatusError",
    "APIRequestFailedError",
    "APIAuthenticationError",
    "APIReachLimitError",
    "APIInternalError",
    "APIServerFlowExceedError",
    "APIResponseError",
    "APIResponseValidationError",
    "APITimeoutError",
    "APIConnectionError",
]


class ZhipuAIError(Exception):
    message: str

    def __init__(self, message: str, ) -> None:
        super().__init__(message)
        self.message = message


class APIStatusError(ZhipuAIError):
    response: httpx.Response
    status_code: int
    request_id: str | None

    def __init__(self, message: str, *, response: httpx.Response) -> None:
        super().__init__(message)
        self.response = response
        self.status_code = response.status_code
        self.request_id = response.headers.get("x-request-id")


class APIRequestFailedError(APIStatusError):
    ...


class APIAuthenticationError(APIStatusError):
    ...


class APIReachLimitError(APIStatusError):
    ...


class APIInternalError(APIStatusError):
    ...


class APIServerFlowExceedError(APIStatusError):
    ...


class APIResponseError(ZhipuAIError):
    message: str
    request: httpx.Request
    json_data: object

    def __init__(self, message: str, request: httpx.Request, json_data: object):
        self.message = message
        self.request = request
        self.json_data = json_data
        super().__init__(message)


class APIResponseValidationError(APIResponseError):
    status_code: int
    response: httpx.Response
    request_id: str | None

    def __init__(
            self,
            response: httpx.Response,
            json_data: object | None, *,
            message: str | None = None
    ) -> None:
        self.response = response
        self.status_code = response.status_code
        self.request_id = response.headers.get("x-request-id")
        if message is None:
            message = "Data returned by API invalid for expected schema."

        if self.request_id:
            message = f"{message.rstrip('.')}, request_id: {self.request_id}"

        super().__init__(
            message=message,
            request=response.request,
            json_data=json_data
        )


class APIConnectionError(APIResponseError):
    def __init__(self, *, message: str | None = None, request: httpx.Request) -> None:
        if message is None:
            message = f"Connection error on {request.url}."
        super().__init__(message, request, json_data=None)


class APITimeoutError(APIConnectionError):
    def __init__(self, request: httpx.Request) -> None:
        super().__init__(message=f"Request timed out on {request.url}.", request=request)
