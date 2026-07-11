import httpx
from zhipuai.core._http_client import HttpClient
from zhipuai.core._errors import APIStatusError
import pytest

def test_make_status_error_parsing():
    client = HttpClient(
        version="1.0.0",
        base_url=httpx.URL("https://example.com"),
        _strict_response_validation=False,
        timeout=None
    )

    # Mock response with JSON error and x-request-id
    response_content = b'{"error": {"message": "Invalid API Key"}}'
    response = httpx.Response(
        401,
        content=response_content,
        headers={"x-request-id": "12345", "Content-Type": "application/json"}
    )

    error = client._make_status_error(response)

    assert isinstance(error, APIStatusError)
    error_msg = str(error)
    assert "401" in error_msg
    assert "Invalid API Key" in error_msg
    assert "12345" in error_msg
