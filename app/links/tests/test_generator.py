import pytest

from django.test import override_settings
from links.generator import generate_token


@pytest.mark.parametrize('token_length', [1, 5, 10])
def test_generated_token_is_indicated_length(token_length):
    with override_settings(TOKEN_LENGTH=token_length):
        generated_token = generate_token(token_length)
    assert len(generated_token) == token_length


def test_generated_token_is_alphanumeric():
    generated_string = generate_token(6)
    assert generated_string.isalnum()


@pytest.mark.parametrize('token_length', [0, -1, -5])
def test_generated_token_raises_error_for_non_positive_length(token_length):
    with override_settings(TOKEN_LENGTH=token_length):
        with pytest.raises(ValueError):
            generate_token(token_length)
