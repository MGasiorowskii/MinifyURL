from links.models import ShortURL


def test_token_is_generated_after_save():
    url = ShortURL.objects.create(original='https://example.com')
    assert url.token
