import httpx
from httpx import URL

from zhipuai.core._errors import (
	APIAuthenticationError,
	APIConnectionError,
	APIInternalError,
	APIReachLimitError,
	APIRequestFailedError,
	APIResponseValidationError,
	APIServerFlowExceedError,
	APITimeoutError,
)
from zhipuai.core._http_client import HttpClient


def test_api_connection_error_url():
	request = httpx.Request('GET', 'https://api.example.com/test-connection')
	err = APIConnectionError(request=request)
	assert 'https://api.example.com/test-connection' in err.message
	assert err.message.endswith(', url: https://api.example.com/test-connection')


def test_api_timeout_error_url():
	request = httpx.Request('POST', 'https://api.example.com/test-timeout')
	err = APITimeoutError(request=request)
	assert 'https://api.example.com/test-timeout' in err.message
	assert err.message.endswith(', url: https://api.example.com/test-timeout')


def test_api_response_validation_error_url():
	request = httpx.Request('GET', 'https://api.example.com/test-validation')
	response = httpx.Response(status_code=200, request=request)
	err = APIResponseValidationError(response=response, json_data={'foo': 'bar'})
	assert 'https://api.example.com/test-validation' in err.message
	assert err.message.endswith(', url: https://api.example.com/test-validation')


def test_http_client_status_error_url():
	# Initialize a simple HttpClient
	client = HttpClient(
		version='1.0.0',
		base_url=URL('https://api.example.com'),
		_strict_response_validation=False,
		timeout=5.0,
	)

	# 400 Request Failed
	request_400 = httpx.Request('GET', 'https://api.example.com/endpoint-400')
	response_400 = httpx.Response(
		status_code=400,
		request=request_400,
		json={'message': 'Invalid parameter value'},
		headers={'x-request-id': 'req-123'},
	)
	err_400 = client._make_status_error(response_400)
	assert isinstance(err_400, APIRequestFailedError)
	assert 'url: https://api.example.com/endpoint-400' in err_400.message
	assert 'request_id: req-123' in err_400.message
	assert 'Error code: 400' in err_400.message
	assert 'Invalid parameter value' in err_400.message

	# 401 Authentication Error
	request_401 = httpx.Request('POST', 'https://api.example.com/endpoint-401')
	response_401 = httpx.Response(
		status_code=401,
		request=request_401,
		json={'msg': 'Unauthorized access'},
		headers={'x-request-id': 'req-456'},
	)
	err_401 = client._make_status_error(response_401)
	assert isinstance(err_401, APIAuthenticationError)
	assert 'url: https://api.example.com/endpoint-401' in err_401.message
	assert 'request_id: req-456' in err_401.message
	assert 'Unauthorized access' in err_401.message

	# 429 Reach Limit Error
	request_429 = httpx.Request('GET', 'https://api.example.com/endpoint-429')
	response_429 = httpx.Response(
		status_code=429,
		request=request_429,
		json={'error': {'message': 'Rate limit exceeded'}},
		headers={'x-request-id': 'req-789'},
	)
	err_429 = client._make_status_error(response_429)
	assert isinstance(err_429, APIReachLimitError)
	assert 'url: https://api.example.com/endpoint-429' in err_429.message
	assert 'request_id: req-789' in err_429.message
	assert 'Rate limit exceeded' in err_429.message

	# 500 Internal Error
	request_500 = httpx.Request('GET', 'https://api.example.com/endpoint-500')
	response_500 = httpx.Response(
		status_code=500,
		request=request_500,
		content=b'Internal Server Error Exception',
	)
	err_500 = client._make_status_error(response_500)
	assert isinstance(err_500, APIInternalError)
	assert 'url: https://api.example.com/endpoint-500' in err_500.message
	assert 'Internal Server Error Exception' in err_500.message

	# 503 Server Flow Exceed Error
	request_503 = httpx.Request('GET', 'https://api.example.com/endpoint-503')
	response_503 = httpx.Response(
		status_code=503,
		request=request_503,
		content=b'Service Unavailable',
	)
	err_503 = client._make_status_error(response_503)
	assert isinstance(err_503, APIServerFlowExceedError)
	assert 'url: https://api.example.com/endpoint-503' in err_503.message
	assert 'Service Unavailable' in err_503.message
