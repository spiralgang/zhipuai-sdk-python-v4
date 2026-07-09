import httpx
import pytest
from zhipuai.core._http_client import HttpClient
from zhipuai.core._errors import APIRequestFailedError

def test_make_status_error_basic():
    client = HttpClient(version="1.0.0", base_url=httpx.URL("https://api.example.com"), _strict_response_validation=False, timeout=60.0)

    # Test with plain text response
    response = httpx.Response(400, content=b"Invalid request", request=httpx.Request("POST", "https://api.example.com"))
    err = client._make_status_error(response)
    assert isinstance(err, APIRequestFailedError)
    assert str(err) == "Error code: 400, with error text Invalid request"

def test_make_status_error_with_request_id():
    client = HttpClient(version="1.0.0", base_url=httpx.URL("https://api.example.com"), _strict_response_validation=False, timeout=60.0)

    # Test with x-request-id header
    headers = {"x-request-id": "12345"}
    response = httpx.Response(400, content=b"Error", headers=headers, request=httpx.Request("POST", "https://api.example.com"))
    err = client._make_status_error(response)
    assert "request_id: 12345" in str(err)

def test_make_status_error_with_json_body_message():
    client = HttpClient(version="1.0.0", base_url=httpx.URL("https://api.example.com"), _strict_response_validation=False, timeout=60.0)

    # Test with JSON response body containing message
    json_content = b'{"error": {"message": "Detailed error message"}}'
    response = httpx.Response(400, content=json_content, request=httpx.Request("POST", "https://api.example.com"))
    err = client._make_status_error(response)
    assert "Detailed error message" in str(err)

def test_make_status_error_with_json_body_msg():
    client = HttpClient(version="1.0.0", base_url=httpx.URL("https://api.example.com"), _strict_response_validation=False, timeout=60.0)

    # Test with JSON response body containing msg
    json_content = b'{"msg": "Alternative error message"}'
    response = httpx.Response(400, content=json_content, request=httpx.Request("POST", "https://api.example.com"))
    err = client._make_status_error(response)
    assert "Alternative error message" in str(err)
