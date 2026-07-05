import httpx
import pytest
from zhipuai.core._http_client import HttpClient
from zhipuai.core import _errors

class MockResponse(httpx.Response):
    def __init__(self, status_code, content=None, headers=None):
        super().__init__(status_code, content=content, headers=headers)
        self._request = httpx.Request("GET", "https://example.com")

def test_make_status_error_with_json_message():
    client = HttpClient(version="1.0.0", base_url="https://example.com", _strict_response_validation=False, timeout=5.0)
    response = MockResponse(
        400,
        content=b'{"error": {"message": "Invalid parameters"}}',
        headers={"content-type": "application/json"}
    )
    error = client._make_status_error(response)
    assert isinstance(error, _errors.APIRequestFailedError)
    assert "Error code: 400, message: Invalid parameters" in str(error)

def test_make_status_error_with_json_msg():
    client = HttpClient(version="1.0.0", base_url="https://example.com", _strict_response_validation=False, timeout=5.0)
    response = MockResponse(
        400,
        content=b'{"msg": "Something went wrong"}',
        headers={"content-type": "application/json"}
    )
    error = client._make_status_error(response)
    assert "Error code: 400, message: Something went wrong" in str(error)

def test_make_status_error_with_request_id():
    client = HttpClient(version="1.0.0", base_url="https://example.com", _strict_response_validation=False, timeout=5.0)
    response = MockResponse(
        500,
        content=b"Internal Server Error",
        headers={"x-request-id": "req_123456"}
    )
    error = client._make_status_error(response)
    assert isinstance(error, _errors.APIInternalError)
    assert "[Request ID: req_123456]" in str(error)

def test_make_status_error_with_plain_text():
    client = HttpClient(version="1.0.0", base_url="https://example.com", _strict_response_validation=False, timeout=5.0)
    response = MockResponse(
        429,
        content=b"Too Many Requests",
    )
    error = client._make_status_error(response)
    assert isinstance(error, _errors.APIReachLimitError)
    assert "Error code: 429, message: Too Many Requests" in str(error)

def test_missing_api_key_error_message():
    from zhipuai import ZhipuAI
    import os

    # Save original API key if it exists
    original_key = os.environ.get("ZHIPUAI_API_KEY")
    if original_key:
        del os.environ["ZHIPUAI_API_KEY"]

    try:
        with pytest.raises(_errors.ZhipuAIError) as excinfo:
            ZhipuAI(api_key=None)
        assert "https://open.bigmodel.cn/" in str(excinfo.value)
        assert "ZHIPUAI_API_KEY" in str(excinfo.value)
    finally:
        # Restore original API key
        if original_key:
            os.environ["ZHIPUAI_API_KEY"] = original_key
