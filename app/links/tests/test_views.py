from collections import defaultdict
from unittest.mock import patch

import pytest

from django.urls import reverse
from links.models import ShortURL
from rest_framework import status

SHORTEN_ENDPOINT_V1 = "v1:short-url"
REDIRECT_ENDPOINT_V1 = "v1:redirect-url"
STATISTICS_ENDPOINT_V1 = "v1:statistics"
LONG_URL = "https://www.example.com"


@pytest.fixture
def short_url():
    return ShortURL.objects.create(original=LONG_URL)


@pytest.fixture
def random_short_urls():
    some_url = "https://www.example.com/{}"
    for i in range(5):
        ShortURL.objects.create(original=some_url.format(i))


@pytest.fixture
def click_logs(short_url):
    short_url.click_count = 3
    short_url.save(update_fields=['click_count'])

    ips = ['8.8.8.8', '127.0.0.1', '192.168.1.1']
    agents = ['Chrome/94.0.4606.71', 'Mozilla/5.0', 'Safari/537.36']

    return [
        short_url.clicks.create(ip_address=ip, user_agent=agent)
        for ip, agent in zip(ips, agents)
    ]


@pytest.fixture
def mock_log_statistics_task():
    with patch('links.tasks.log_statistics.delay') as mock_log_statistics:
        yield mock_log_statistics


def test_shorten_view_create_short_url(client):
    body = {"original": LONG_URL}
    url = reverse(f'{SHORTEN_ENDPOINT_V1}-list')
    response = client.post(url, body)

    expected_short_url = ShortURL.objects.get(original=LONG_URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["short_url"] == expected_short_url.url


def test_shorten_view_returns_short_url_if_exists(client, short_url):
    body = {"original": LONG_URL}
    url = reverse(f'{SHORTEN_ENDPOINT_V1}-list')
    response = client.post(url, body)

    assert ShortURL.objects.filter(original=LONG_URL).count() == 1
    assert response.status_code == status.HTTP_200_OK
    assert response.data["short_url"] == short_url.url


def test_redirect_view_redirects(client, short_url, mock_log_statistics_task):
    url = reverse(REDIRECT_ENDPOINT_V1, args=(short_url.token,))
    response = client.get(url)

    assert response.status_code == status.HTTP_302_FOUND
    assert response['Location'] == LONG_URL
    assert mock_log_statistics_task.called


def test_redirect_view_return_404_when_link_not_exists(
    client, mock_log_statistics_task
):
    non_existing_token = "non-existing-token"
    assert not ShortURL.objects.filter(token=non_existing_token).exists()

    url = reverse(REDIRECT_ENDPOINT_V1, args=(non_existing_token,))
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert not mock_log_statistics_task.called


def test_redirect_view_log_clicks(
    client, mock_redis, short_url, mock_log_statistics_task
):
    assert short_url.clicks.count() == 0

    key = f"clicks:{short_url.token}"
    url = reverse(REDIRECT_ENDPOINT_V1, args=(short_url.token,))
    client.get(url)
    short_url.refresh_from_db()
    assert int(mock_redis.get(key)) == 1
    assert mock_log_statistics_task.call_count == 1

    client.get(url)
    short_url.refresh_from_db()
    assert int(mock_redis.get(key)) == 2
    assert mock_log_statistics_task.call_count == 2


def test_statistics_list_return_blank_list_for_no_logs(client):
    url = reverse(f'{STATISTICS_ENDPOINT_V1}-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


def test_statistics_list_return_aggregated_logs(
    client, click_logs, short_url, random_short_urls
):
    click_data = defaultdict(
        lambda: {"click_count": 0, "ip_addresses": [], "user_agents": []}
    )
    click_data[0] = dict(
        click_count=short_url.click_count,
        ip_addresses=[log.ip_address for log in click_logs],
        user_agents=[log.user_agent for log in click_logs],
    )

    url = reverse(f'{STATISTICS_ENDPOINT_V1}-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == [click_data[i] for i in range(6)]


def test_statistics_detail_return_404_for_not_existing_token(client):
    non_existing_token = "non-existing-token"
    url = reverse(f'{STATISTICS_ENDPOINT_V1}-detail', args=(non_existing_token,))
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_statistics_detail_return_aggregated_logs(
    client, click_logs, short_url, mock_redis
):
    fresh_clicks = 3
    mock_redis.set(f"clicks:{short_url.token}", fresh_clicks)

    url = reverse(f'{STATISTICS_ENDPOINT_V1}-detail', args=(short_url.token,))
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "click_count": short_url.click_count + fresh_clicks,
        "ip_addresses": [log.ip_address for log in click_logs],
        'user_agents': [log.user_agent for log in click_logs],
    }


def test_num_of_queries_on_shorten_view(
    client, random_short_urls, django_assert_num_queries
):
    body = {"original": LONG_URL}
    url = reverse(f'{SHORTEN_ENDPOINT_V1}-list')
    with django_assert_num_queries(5):
        """
        1. SELECT "links_shorturl"
        2. SAVEPOINT
        3. INSERT INTO "links_shorturl"
        4. UPDATE "links_shorturl"
        5. RELEASE SAVEPOINT
        """
        client.post(url, body)


def test_num_of_queries_on_shorten_view_if_short_url_exists(
    client, random_short_urls, short_url, django_assert_num_queries
):
    body = {"original": LONG_URL}
    url = reverse(f'{SHORTEN_ENDPOINT_V1}-list')
    with django_assert_num_queries(1):
        """
        1. SELECT "links_shorturl"
        """
        client.post(url, body)


def test_num_of_queries_on_redirect_view(
    client, short_url, django_assert_num_queries, mock_log_statistics_task
):
    url = reverse(REDIRECT_ENDPOINT_V1, args=(short_url.token,))
    with django_assert_num_queries(1):
        """
        1. SELECT "links_shorturl"
        """
        client.get(url)


def test_num_of_queries_on_statistics_view(
    client, short_url, random_short_urls, django_assert_num_queries
):
    url = reverse(f'{STATISTICS_ENDPOINT_V1}-list')
    with django_assert_num_queries(1):
        """
        1. SELECT "links_shorturl"
        """
        client.get(url)
