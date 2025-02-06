import pytest

from django.urls import reverse
from links.models import ShortURL
from rest_framework import status

SHORT_URL_ENDPOINT_V1 = "v1:short-url"
REDIRECT_TO_ORIGINAL_LINK_ENDPOINT_V1 = "v1:redirect-to-original-link"
STATISTICS_ENDPOINT_V1 = "v1:statistics"
LONG_URL = "https://www.example.com"


@pytest.fixture
def short_url():
    return ShortURL.objects.create(original=LONG_URL)


@pytest.fixture
def logs(short_url):
    short_url.click_count = 3
    short_url.save(update_fields=['click_count'])

    ips = ['8.8.8.8', '127.0.0.1', '192.168.1.1']
    agents = ['Chrome/94.0.4606.71', 'Mozilla/5.0', 'Safari/537.36']

    return [
        short_url.clicks.create(ip_address=ip, user_agent=agent)
        for ip, agent in zip(ips, agents)
    ]


def test_create_short_url(client):
    body = {"original": LONG_URL}
    url = reverse(f'{SHORT_URL_ENDPOINT_V1}-list')
    response = client.post(url, body)

    expected_short_url = ShortURL.objects.get(original=LONG_URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["short_url"] == expected_short_url.url


def test_view_returns_short_url_if_exists(client, short_url):
    body = {"original": LONG_URL}
    url = reverse(f'{SHORT_URL_ENDPOINT_V1}-list')
    response = client.post(url, body)

    assert ShortURL.objects.filter(original=LONG_URL).count() == 1
    assert response.status_code == status.HTTP_200_OK
    assert response.data["short_url"] == short_url.url


def test_redirect_to_original_link_redirects(client, short_url):
    url = reverse(REDIRECT_TO_ORIGINAL_LINK_ENDPOINT_V1, args=(short_url.token,))
    response = client.get(url)

    assert response.status_code == status.HTTP_302_FOUND
    assert response['Location'] == LONG_URL


def test_redirect_to_original_link_return_404_when_link_not_exists(client):
    non_existing_token = "non-existing-token"
    assert not ShortURL.objects.filter(token=non_existing_token).exists()

    url = reverse(REDIRECT_TO_ORIGINAL_LINK_ENDPOINT_V1, args=(non_existing_token,))
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_redirect_to_original_link_log_clicks(client, short_url):
    assert short_url.click_count == 0
    assert short_url.clicks.count() == 0

    url = reverse(REDIRECT_TO_ORIGINAL_LINK_ENDPOINT_V1, args=(short_url.token,))
    client.get(url)
    short_url.refresh_from_db()
    assert short_url.click_count == 1
    assert short_url.clicks.count() == 1

    client.get(url)
    short_url.refresh_from_db()
    assert short_url.click_count == 2
    assert short_url.clicks.count() == 2


def test_statistics_list_return_blank_list_for_no_logs(client):
    url = reverse(f'{STATISTICS_ENDPOINT_V1}-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


def test_statistics_list_return_aggregated_logs(client, logs, short_url):
    url = reverse(f'{STATISTICS_ENDPOINT_V1}-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        {
            "click_count": short_url.click_count,
            "ip_addresses": [log.ip_address for log in logs],
            'user_agents': [log.user_agent for log in logs],
        }
    ]


def test_statistics_detail_return_404_for_not_existing_token(client):
    non_existing_token = "non-existing-token"
    url = reverse(f'{STATISTICS_ENDPOINT_V1}-detail', args=(non_existing_token,))
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_statistics_detail_return_aggregated_logs(client, logs, short_url):
    url = reverse(f'{STATISTICS_ENDPOINT_V1}-detail', args=(short_url.token,))
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "click_count": short_url.click_count,
        "ip_addresses": [log.ip_address for log in logs],
        'user_agents': [log.user_agent for log in logs],
    }
