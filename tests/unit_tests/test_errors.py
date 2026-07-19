from httpx import URL, Headers, Request, Response

from zhipuai.core._errors import (
	APIConnectionError,
	APIResponseValidationError,
	APITimeoutError,
)
from zhipuai.core._http_client import HttpClient


def test_api_response_validation_error_url():
	request = Request(method='GET', url='https://api.zhipu.cn/v4/chat/completions')
	response = Response(status_code=200, request=request)

	err = APIResponseValidationError(response=response, json_data={'foo': 'bar'})

	assert 'url: https://api.zhipu.cn/v4/chat/completions' in err.message
	assert 'Data returned by API invalid for expected schema.' in err.message


def test_api_connection_error_url():
	request = Request(method='POST', url='https://api.zhipu.cn/v4/images/generations')

	err = APIConnectionError(request=request)

	assert 'url: https://api.zhipu.cn/v4/images/generations' in err.message
	assert 'Connection error.' in err.message


def test_api_timeout_error_url():
	request = Request(method='POST', url='https://api.zhipu.cn/v4/embeddings')

	err = APITimeoutError(request=request)

	assert 'url: https://api.zhipu.cn/v4/embeddings' in err.message
	assert 'Request timed out.' in err.message


def test_http_client_make_status_error_url():
	client = HttpClient(
		version='2.1.5',
		base_url=URL('https://api.zhipu.cn/'),
		_strict_response_validation=False,
		timeout=5.0,
	)

	request = Request(method='GET', url='https://api.zhipu.cn/v4/fine_tuning/jobs')
	response = Response(
		status_code=400,
		request=request,
		headers=Headers({'x-request-id': 'req-123456'}),
		content=b'{"error": {"message": "Invalid request parameters."}}',
	)

	err = client._make_status_error(response)

	assert 'Error code: 400' in err.message
	assert 'message: Invalid request parameters.' in err.message
	assert 'request_id: req-123456' in err.message
	assert 'url: https://api.zhipu.cn/v4/fine_tuning/jobs' in err.message
