# -*- coding: utf-8 -*-
import pytest
import httpx
from typing import Iterable, Type, cast
from zhipuai.core import HttpClient, StreamResponse, get_args, APIResponseError
from zhipuai.core._base_type import ResponseT
from zhipuai.types.chat.chat_completion_chunk import ChatCompletionChunk

class MockClient:
    _strict_response_validation: bool = False
    def _process_response_data(
        self,
        *,
        data: object,
        cast_type: Type[ResponseT],
        response: httpx.Response,
    ) -> ResponseT:
        pass

def test_stream_error_handling_detailed() -> None:
    def body() -> Iterable[bytes]:
        yield b'data: {"error": {"message": "Specific API error message", "code": "invalid_request_error"}}\n\n'

    _stream_cls = StreamResponse[ChatCompletionChunk]
    http_response = httpx.Response(status_code=200, content=body())
    http_response.request = httpx.Request("POST", "https://example.com")

    stream_cls = _stream_cls(
        cast_type=cast(type, get_args(_stream_cls)[0]),
        response=http_response,
        client=MockClient(),
    )

    with pytest.raises(APIResponseError) as excinfo:
        next(stream_cls)

    assert str(excinfo.value) == "Specific API error message"
    assert excinfo.value.json_data == {"message": "Specific API error message", "code": "invalid_request_error"}

def test_stream_error_handling_generic() -> None:
    def body() -> Iterable[bytes]:
        yield b'data: {"error": {"code": "unknown_error"}}\n\n'

    _stream_cls = StreamResponse[ChatCompletionChunk]
    http_response = httpx.Response(status_code=200, content=body())
    http_response.request = httpx.Request("POST", "https://example.com")

    stream_cls = _stream_cls(
        cast_type=cast(type, get_args(_stream_cls)[0]),
        response=http_response,
        client=MockClient(),
    )

    with pytest.raises(APIResponseError) as excinfo:
        next(stream_cls)

    assert str(excinfo.value) == "An error occurred during streaming"
    assert excinfo.value.json_data == {"code": "unknown_error"}

def test_stream_error_event() -> None:
    def body() -> Iterable[bytes]:
        yield b'event: error\n'
        yield b'data: {"error": {"message": "Error event message"}}\n\n'

    _stream_cls = StreamResponse[ChatCompletionChunk]
    http_response = httpx.Response(status_code=200, content=body())
    http_response.request = httpx.Request("POST", "https://example.com")

    stream_cls = _stream_cls(
        cast_type=cast(type, get_args(_stream_cls)[0]),
        response=http_response,
        client=MockClient(),
    )

    with pytest.raises(APIResponseError) as excinfo:
        next(stream_cls)

    assert str(excinfo.value) == "Error event message"
