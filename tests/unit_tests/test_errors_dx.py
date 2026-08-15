from __future__ import annotations

import httpx

from zhipuai.core._errors import (
	APIConnectionError,
	APIRequestFailedError,
	APIResponseValidationError,
	APIStatusError,
	APITimeoutError,
	ZhipuAIError,
)
from zhipuai.core._http_client import HttpClient


def test_api_response_validation_error_incorporates_url_and_request_id():
	request = httpx.Request('POST', 'https://api.example.com/v4/chat/completions')
	headers = httpx.Headers({'x-request-id': 'req-validation-123'})
	response = httpx.Response(200, request=request, headers=headers)

	# Test with default message
	err_default = APIResponseValidationError(response=response, json_data=None)
	assert err_default.request_id == 'req-validation-123'
	assert 'Data returned by API invalid for expected schema' in err_default.message
	assert 'url: https://api.example.com/v4/chat/completions' in err_default.message

	# Test with custom message
	err_custom = APIResponseValidationError(
		response=response, json_data=None, message='Custom schema error.'
	)
	assert err_custom.request_id == 'req-validation-123'
	assert 'Custom schema error' in err_custom.message
	assert 'url: https://api.example.com/v4/chat/completions' in err_custom.message


def test_api_connection_error_incorporates_url():
	request = httpx.Request('GET', 'https://api.example.com/v4/files')
	err = APIConnectionError(request=request)
	assert 'Connection error' in err.message
	assert 'url: https://api.example.com/v4/files' in err.message


def test_api_timeout_error_incorporates_url():
	request = httpx.Request('GET', 'https://api.example.com/v4/timeout')
	err = APITimeoutError(request=request)
	assert 'Request timed out' in err.message
	assert 'url: https://api.example.com/v4/timeout' in err.message


def test_http_client_make_status_error_incorporates_url_and_request_id():
	# Instantiate a minimal HttpClient
	client = HttpClient(
		version='1.0.0',
		base_url=httpx.URL('https://open.bigmodel.cn/api/paas/v4/'),
		_strict_response_validation=False,
		timeout=5.0,
	)

	request = httpx.Request(
		'POST', 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
	)
	headers = httpx.Headers(
		{
			'x-request-id': 'req-status-456',
			'content-type': 'application/json',
		}
	)
	response = httpx.Response(
		400,
		request=request,
		headers=headers,
		json={'error': {'message': 'Invalid API Key supplied'}},
	)

	status_error = client._make_status_error(response)
	assert status_error.status_code == 400
	assert status_error.request_id == 'req-status-456'
	assert 'Error code: 400' in status_error.message
	assert 'message: Invalid API Key supplied' in status_error.message
	assert 'request_id: req-status-456' in status_error.message
	expected_url = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
	assert f'url: {expected_url}' in status_error.message


def test_exception_repr():
	z_err = ZhipuAIError('Base error message')
	assert repr(z_err) == "ZhipuAIError(message='Base error message')"

	req = httpx.Request('POST', 'https://api.example.com/v4/chat/completions')
	headers = httpx.Headers({'x-request-id': 'req-repr-789'})
	resp = httpx.Response(400, request=req, headers=headers)

	status_err = APIStatusError('Status error message', response=resp)
	expected_status = (
		"APIStatusError(message='Status error message',"
		" status_code=400, request_id='req-repr-789')"
	)
	assert repr(status_err) == expected_status

	subclass_err = APIRequestFailedError('Request failed message', response=resp)
	expected_subclass = (
		"APIRequestFailedError(message='Request failed message',"
		" status_code=400, request_id='req-repr-789')"
	)
	assert repr(subclass_err) == expected_subclass
