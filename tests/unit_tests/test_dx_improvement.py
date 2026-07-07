import httpx
import pytest
from zhipuai.core._http_client import HttpClient
from zhipuai.core._errors import APIRequestFailedError
from httpx import URL

def test_make_status_error_improvement():
    client = HttpClient(version="test", base_url=URL("https://example.com"), _strict_response_validation=False, timeout=5.0)

    # Case 1: Nested error message and request ID
    response1 = httpx.Response(
        400,
        content=b'{"error": {"message": "Invalid API Key", "code": "invalid_key"}}',
        headers={"x-request-id": "req_123", "Content-Type": "application/json"}
    )
    err1 = client._make_status_error(response1)
    msg1 = str(err1)
    print(f"\nError 1: {msg1}")
    assert "Error code: 400 - Invalid API Key (Request ID: req_123)" in msg1

    # Case 2: Top-level message
    response2 = httpx.Response(
        401,
        content=b'{"message": "Unauthorized access"}',
        headers={"Content-Type": "application/json"}
    )
    err2 = client._make_status_error(response2)
    msg2 = str(err2)
    print(f"Error 2: {msg2}")
    assert "Error code: 401 - Unauthorized access" in msg2
    assert "Request ID" not in msg2

    # Case 3: Top-level msg field
    response3 = httpx.Response(
        429,
        content=b'{"msg": "Too many requests"}',
        headers={"x-request-id": "req_456", "Content-Type": "application/json"}
    )
    err3 = client._make_status_error(response3)
    msg3 = str(err3)
    print(f"Error 3: {msg3}")
    assert "Error code: 429 - Too many requests (Request ID: req_456)" in msg3

    # Case 4: Non-JSON response
    response4 = httpx.Response(
        500,
        content=b"Internal Server Error Text",
        headers={"x-request-id": "req_789"}
    )
    err4 = client._make_status_error(response4)
    msg4 = str(err4)
    print(f"Error 4: {msg4}")
    assert "Error code: 500, with error text Internal Server Error Text (Request ID: req_789)" in msg4
