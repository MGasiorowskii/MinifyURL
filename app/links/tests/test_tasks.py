from links.models import ShortURL
from links.tasks import sync_clicks_to_db


def test_sync_clicks_to_db(mock_redis):
    original_url = "http://example.com"
    short_url = ShortURL.objects.create(original=original_url, click_count=2)

    mock_redis.set(f"clicks:{short_url.token}", 3)
    sync_clicks_to_db()

    short_url.refresh_from_db()
    assert short_url.click_count == 5

    assert not mock_redis.exists(f"clicks:{short_url}")
