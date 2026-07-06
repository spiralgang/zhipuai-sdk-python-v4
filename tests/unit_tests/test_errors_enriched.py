import httpx
import json
from zhipuai.core._http_client import HttpClient
from httpx import Response, Request, URL

def test_make_status_error_enriched_message():
    client = HttpClient(
        version="1.0.0",
        base_url=URL("https://api.example.com"),
        _strict_response_validation=False,
        timeout=5.0
    )

    # Test nested error message and request-id
    error_data = {"error": {"message": "Invalid API Key", "code": "invalid_api_key"}}
    response = Response(
        status_code=401,
        content=json.dumps(error_data).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-request-id": "req-123"},
        request=Request("POST", "https://api.example.com/chat")
    )

    error = client._make_status_error(response)
    assert "Invalid API Key" in str(error.args[0])
    assert "req-123" in str(error.args[0])

def test_make_status_error_flat_message():
    client = HttpClient(
        version="1.0.0",
        base_url=URL("https://api.example.com"),
        _strict_response_validation=False,
        timeout=5.0
    )

    # Test flat message
    error_data = {"message": "Rate limit exceeded"}
    response = Response(
        status_code=429,
        content=json.dumps(error_data).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-request-id": "req-456"},
        request=Request("POST", "https://api.example.com/chat")
    )
    error = client._make_status_error(response)
    assert "Rate limit exceeded" in str(error.args[0])
    assert "req-456" in str(error.args[0])

def test_make_status_error_non_json():
    client = HttpClient(
        version="1.0.0",
        base_url=URL("https://api.example.com"),
        _strict_response_validation=False,
        timeout=5.0
    )

    # Test non-json response
    response = Response(
        status_code=500,
        content=b"Internal Server Error",
        headers={"Content-Type": "text/plain", "x-request-id": "req-789"},
        request=Request("POST", "https://api.example.com/chat")
    )
    error = client._make_status_error(response)
    assert "Internal Server Error" in str(error.args[0])
    assert "req-789" in str(error.args[0])
