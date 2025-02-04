import pytest

from links.generator import DOMAIN, _generate_token, generate_short_link
from links.models import ShortURL


@pytest.mark.parametrize('string_length', [1, 5, 10])
def test_generated_token_is_indicated_length(string_length):
    generated_string = _generate_token(string_length)
    assert len(generated_string) == string_length


def test_generated_token_is_alphanumeric():
    string_length = 6
    generated_string = _generate_token(string_length)
    assert generated_string.isalnum()


@pytest.mark.parametrize('string_length', [0, -1, -5])
def test_generated_token_raises_error_for_non_positive_length(string_length):
    with pytest.raises(ValueError):
        _generate_token(string_length)


def test_generate_short_link_creates_short_link():
    original_url = 'https://www.example.com'
    short_link = generate_short_link(original_url)
    token = short_link.split('/')[-1]

    assert short_link.startswith(f'https://{DOMAIN}')
    assert ShortURL.objects.filter(alias=token, original=original_url).exists()
