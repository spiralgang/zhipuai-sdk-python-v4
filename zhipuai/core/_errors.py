from __future__ import annotations

import httpx

__all__ = [
	'ZhipuAIError',
	'APIStatusError',
	'APIRequestFailedError',
	'APIAuthenticationError',
	'APIReachLimitError',
	'APIInternalError',
	'APIServerFlowExceedError',
	'APIResponseError',
	'APIResponseValidationError',
	'APITimeoutError',
	'APIConnectionError',
]


class ZhipuAIError(Exception):
	message: str

	def __init__(
		self,
		message: str,
	) -> None:
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
		self.request_id = response.headers.get('x-request-id')


class APIRequestFailedError(APIStatusError): ...


class APIAuthenticationError(APIStatusError): ...


class APIReachLimitError(APIStatusError): ...


class APIInternalError(APIStatusError): ...


class APIServerFlowExceedError(APIStatusError): ...


class APIResponseError(ZhipuAIError):
	message: str
	request: httpx.Request
	json_data: object

	def __init__(self, message: str, request: httpx.Request, json_data: object):
		self.request = request
		self.json_data = json_data
		url = getattr(request, 'url', None)
		if url is not None:
			url_str = str(url)
			if url_str and f', url: {url_str}' not in message:
				message = f'{message}, url: {url_str}'
		self.message = message
		super().__init__(message)


class APIResponseValidationError(APIResponseError):
	status_code: int
	response: httpx.Response
	request_id: str | None

	def __init__(
		self,
		response: httpx.Response,
		json_data: object | None,
		*,
		message: str | None = None,
	) -> None:
		super().__init__(
			message=message or 'Data returned by API invalid for expected schema.',
			request=response.request,
			json_data=json_data,
		)
		self.response = response
		self.status_code = response.status_code
		self.request_id = response.headers.get('x-request-id')


class APIConnectionError(APIResponseError):
	def __init__(
		self, *, message: str = 'Connection error.', request: httpx.Request
	) -> None:
		super().__init__(message, request, json_data=None)


class APITimeoutError(APIConnectionError):
	def __init__(self, request: httpx.Request) -> None:
		super().__init__(message='Request timed out.', request=request)
