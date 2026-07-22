from httpx import URL, Headers, Request, Response

from zhipuai.core._errors import (
	APIConnectionError,
	APIResponseValidationError,
	APITimeoutError,
)
from zhipuai.core._http_client import HttpClient


def test_api_response_validation_error_formatting():
	request = Request(method='GET', url='https://api.example.com/v4/chat/completions')
	headers = Headers({'x-request-id': 'req_validation_123'})
	response = Response(200, headers=headers, request=request)

	err = APIResponseValidationError(
		response=response,
		json_data={'invalid_field': 'data'},
		message='Custom validation message',
	)

	assert 'Custom validation message' in err.message
	assert ', url: https://api.example.com/v4/chat/completions' in err.message
	assert err.request_id == 'req_validation_123'
	assert err.status_code == 200


def test_api_connection_error_formatting():
	request = Request(method='POST', url='https://api.example.com/v4/embeddings')
	err = APIConnectionError(request=request)

	assert 'Connection error' in err.message
	assert ', url: https://api.example.com/v4/embeddings' in err.message


def test_api_timeout_error_formatting():
	request = Request(
		method='POST', url='https://api.example.com/v4/images/generations'
	)
	err = APITimeoutError(request=request)

	assert 'Request timed out' in err.message
	assert ', url: https://api.example.com/v4/images/generations' in err.message


def test_http_client_make_status_error_formatting():
	client = HttpClient(
		version='2.1.5',
		base_url=URL('https://api.zhipu.cn/'),
		_strict_response_validation=False,
		timeout=5.0,
	)

	request = Request(method='GET', url='https://api.zhipu.cn/v4/chat/completions')
	headers = Headers({'x-request-id': 'req_status_456'})
	# Mock 400 Bad Request
	response = Response(
		400,
		headers=headers,
		request=request,
		json={'error': {'message': 'Invalid API Key'}},
	)

	err = client._make_status_error(response)

	assert 'Error code: 400' in err.message
	assert 'message: Invalid API Key' in err.message
	assert ', url: https://api.zhipu.cn/v4/chat/completions' in err.message
	assert 'request_id: req_status_456' in err.message
	assert err.request_id == 'req_status_456'
	assert err.status_code == 400
