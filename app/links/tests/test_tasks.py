from links.models import ShortURL
from links.tasks import log_statistics, sync_clicks_to_db


def test_sync_clicks_to_db(mock_redis):
    original_url = "http://example.com"
    short_url = ShortURL.objects.create(original=original_url, click_count=2)

    mock_redis.set(f"clicks:{short_url.token}", 3)
    sync_clicks_to_db()

    short_url.refresh_from_db()
    assert short_url.click_count == 5

    assert not mock_redis.exists(f"clicks:{short_url}")


def test_log_statistics(mock_redis):
    short_url = ShortURL.objects.create(original='https://example.com')
    request_meta_data = {
        'CONTENT_TYPE': 'application/json',
        'HTTP_COOKIE': '',
        'HTTP_X_FORWARDED_FOR': '192.168.1.1',
        'REMOTE_ADDR': '127.0.0.1',
        'REQUEST_METHOD': 'GET',
        'SERVER_NAME': 'testserver',
        'SERVER_PORT': '80',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'HTTP_USER_AGENT': 'Mozilla/5.0',
    }
    log_statistics(request_meta_data, short_url.id)

    short_url.refresh_from_db()
    assert short_url.clicks.count() == 1
    assert short_url.clicks.first().ip_address == '192.168.1.1'
    assert short_url.clicks.first().user_agent == 'Mozilla/5.0'
