import string

from unittest.mock import patch

import pytest

from django.test import override_settings
from links import base62


@pytest.fixture
def mock_hash_settings(monkeypatch, settings):
    length = 4
    settings.SECRET_HASH_KEY = string.ascii_letters + string.digits
    settings.HASH_BASE = 62
    settings.TOKEN_LENGTH = length

    monkeypatch.setattr("links.base62.MAX_INDEX", 62**length)


@pytest.mark.parametrize(
    'index, expected_token', [(1, 'aaaa'), (100, 'aabL'), (1000, 'aaqh')]
)
def test_encode_token(index, expected_token, mock_hash_settings):
    generated_token = base62.encode(index)
    assert generated_token == expected_token
    assert len(generated_token) == 4


@pytest.mark.parametrize(
    'token, expected_index', [('aaaa', 1), ('aabL', 100), ('aaqh', 1000)]
)
def test_decode_token(token, expected_index, mock_hash_settings):
    decoded_index = base62.decode(token)
    assert decoded_index == expected_index


def test_token_encoding_and_decoding_is_bijective():
    original_index = 2025
    generated_token = base62.encode(original_index)
    decoded_index = base62.decode(generated_token)
    assert decoded_index == original_index


@pytest.mark.parametrize('token_length', [0, -1])
def test_encode_raises_error_for_non_positive_index(token_length):
    with override_settings(TOKEN_LENGTH=token_length):
        with pytest.raises(ValueError):
            base62.encode(token_length)


def test_encode_raises_error_for_index_out_of_range():
    with patch('links.base62.MAX_INDEX', 62):
        with pytest.raises(ValueError):
            base62.encode(63)
