import httpx
from httpx import URL

from zhipuai.core._errors import (
	APIConnectionError,
	APIRequestFailedError,
	APIResponseValidationError,
	APITimeoutError,
)
from zhipuai.core._http_client import HttpClient


def test_api_connection_error_url():
	req = httpx.Request(method='GET', url='https://example.com/api/test')
	err = APIConnectionError(request=req)
	assert 'https://example.com/api/test' in err.message
	assert 'url: https://example.com/api/test' in err.message


def test_api_timeout_error_url():
	req = httpx.Request(method='GET', url='https://example.com/api/timeout')
	err = APITimeoutError(request=req)
	assert 'https://example.com/api/timeout' in err.message
	assert 'url: https://example.com/api/timeout' in err.message


def test_api_response_validation_error():
	req = httpx.Request(method='POST', url='https://example.com/api/validate')
	resp = httpx.Response(
		status_code=200, request=req, headers={'x-request-id': 'req-val-123'}
	)
	err = APIResponseValidationError(response=resp, json_data={'foo': 'bar'})
	assert err.request_id == 'req-val-123'
	assert 'https://example.com/api/validate' in err.message
	assert 'url: https://example.com/api/validate' in err.message


def test_make_status_error_with_url_and_request_id():
	req = httpx.Request(method='GET', url='https://example.com/api/status')
	resp = httpx.Response(
		status_code=400,
		request=req,
		json={'message': 'invalid request parameters'},
		headers={'x-request-id': 'req-status-456'},
	)

	client = HttpClient(
		version='v1',
		base_url=URL('https://example.com/'),
		_strict_response_validation=False,
		timeout=5.0,
	)
	err = client._make_status_error(resp)
	assert isinstance(err, APIRequestFailedError)
	assert 'Error code: 400' in err.message
	assert 'invalid request parameters' in err.message
	assert 'request_id: req-status-456' in err.message
	assert 'url: https://example.com/api/status' in err.message
