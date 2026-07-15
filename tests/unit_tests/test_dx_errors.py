import httpx
import pytest
from zhipuai.core._http_client import HttpClient
from zhipuai.core._errors import APIStatusError, APIConnectionError, APITimeoutError
from zhipuai.core._request_opt import FinalRequestOptions

def test_status_error_message_manual():
    response = httpx.Response(400, content=b"Bad Request", request=httpx.Request("GET", "https://api.example.com/test"))
    client = HttpClient(
        version="1.2.3",
        base_url=httpx.URL("https://api.example.com"),
        _strict_response_validation=False,
        timeout=5.0
    )
    err = client._make_status_error(response)
    assert "https://api.example.com/test" in str(err)
    assert "400" in str(err)
    assert "url:" in str(err)

def test_connection_error_message_manual():
    request = httpx.Request("GET", "https://api.example.com/test")
    err = APIConnectionError(request=request)
    assert "https://api.example.com/test" in str(err)
    assert "Connection error," in str(err)
    assert "url:" in str(err)

def test_timeout_error_message_manual():
    request = httpx.Request("GET", "https://api.example.com/test")
    err = APITimeoutError(request=request)
    assert "https://api.example.com/test" in str(err)
    assert "Request timed out," in str(err)
    assert "url:" in str(err)
