import jwt
import pytest

from zhipuai.core._errors import ZhipuAIError
from zhipuai.core._jwt_token import generate_token


def test_token() -> None:
	# 生成token
	token = generate_token('12345678.abcdefg')
	assert token is not None

	# 解析token
	payload = jwt.decode(
		token,
		'abcdefg',
		algorithms='HS256',
		options={'verify_signature': False},
	)
	assert payload is not None
	assert payload.get('api_key') == '12345678'

	apikey = 'invalid_api_key'
	with pytest.raises(ZhipuAIError) as exc_info:
		generate_token(apikey)
	assert 'Invalid API key format' in str(exc_info.value)
	assert 'id>.<secret>' in str(exc_info.value)
