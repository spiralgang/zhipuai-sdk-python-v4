import httpx

from zhipuai.core._errors import (
	APIConnectionError,
	APIResponseError,
	APIResponseValidationError,
	APIStatusError,
	APITimeoutError,
)
from zhipuai.core._http_client import HttpClient


def test_api_response_error_includes_url():
	request = httpx.Request('GET', 'https://example.com/api/test')
	err = APIResponseError(
		message='Oops', request=request, json_data={'detail': 'some error'}
	)
	assert 'url: https://example.com/api/test' in err.message
	assert err.message == 'Oops, url: https://example.com/api/test'


def test_api_connection_error_includes_url():
	request = httpx.Request('GET', 'https://example.com/api/test')
	err = APIConnectionError(message='Connection lost.', request=request)
	assert 'url: https://example.com/api/test' in err.message
	assert err.message == 'Connection lost., url: https://example.com/api/test'


def test_api_timeout_error_includes_url():
	request = httpx.Request('GET', 'https://example.com/api/test')
	err = APITimeoutError(request=request)
	assert 'url: https://example.com/api/test' in err.message
	assert err.message == 'Request timed out., url: https://example.com/api/test'


def test_api_response_validation_error_includes_url_and_request_id():
	request = httpx.Request('GET', 'https://example.com/api/test')
	response = httpx.Response(
		status_code=200, request=request, headers={'x-request-id': 'req-abc-123'}
	)
	err = APIResponseValidationError(
		response=response, json_data={'detail': 'some bad schema'}
	)
	assert 'url: https://example.com/api/test' in err.message
	assert err.request_id == 'req-abc-123'


def test_make_status_error_includes_url_and_request_id():
	client = HttpClient(
		version='2.0.0',
		base_url=httpx.URL('https://example.com'),
		_strict_response_validation=True,
		timeout=10.0,
	)
	request = httpx.Request('POST', 'https://example.com/api/chat')
	response = httpx.Response(
		status_code=400,
		request=request,
		headers={'x-request-id': 'req-9876'},
		json={'error': {'message': 'Invalid prompt format'}},
	)
	err = client._make_status_error(response)

	assert isinstance(err, APIStatusError)
	assert err.status_code == 400
	assert err.request_id == 'req-9876'
	assert 'url: https://example.com/api/chat' in err.message
	assert 'request_id: req-9876' in err.message
	assert 'message: Invalid prompt format' in err.message
