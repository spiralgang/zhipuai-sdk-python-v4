import httpx

from zhipuai.core._errors import (
	APIConnectionError,
	APIRequestFailedError,
	APIResponseValidationError,
	APITimeoutError,
)
from zhipuai.core._http_client import HttpClient


def test_api_connection_error_url():
	request = httpx.Request('GET', 'https://api.example.com/v1/test')
	err = APIConnectionError(request=request)
	assert 'https://api.example.com/v1/test' in err.message
	assert 'url:' in err.message


def test_api_timeout_error_url():
	request = httpx.Request('POST', 'https://api.example.com/v1/timeout')
	err = APITimeoutError(request=request)
	assert 'https://api.example.com/v1/timeout' in err.message
	assert 'url:' in err.message


def test_api_response_validation_error_url():
	request = httpx.Request('GET', 'https://api.example.com/v1/validate')
	response = httpx.Response(200, request=request)
	err = APIResponseValidationError(response=response, json_data={'key': 'val'})
	assert 'https://api.example.com/v1/validate' in err.message
	assert 'url:' in err.message


def test_http_client_status_error_url_and_request_id():
	# We construct a mock HttpClient just to call _make_status_error
	client = HttpClient(
		version='1.0.0',
		base_url=httpx.URL('https://api.example.com/'),
		_strict_response_validation=True,
		timeout=5.0,
	)

	request = httpx.Request('POST', 'https://api.example.com/v1/status_err')
	response = httpx.Response(
		status_code=400,
		request=request,
		headers={'x-request-id': 'req_abc123'},
		json={'error': {'message': 'Invalid parameters'}},
	)

	err = client._make_status_error(response)
	assert isinstance(err, APIRequestFailedError)
	assert 'Invalid parameters' in err.message
	assert 'request_id: req_abc123' in err.message
	assert 'url: https://api.example.com/v1/status_err' in err.message
