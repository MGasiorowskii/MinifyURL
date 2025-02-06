import pytest

from django.urls import reverse
from links.models import ShortURL
from rest_framework import status

SHORT_URL_ENDPOINT_V1 = "v1:short-url"
RETRIEVE_ORIGINAL_LINK_ENDPOINT = "v1:redirect-to-original-link"
LONG_URL = "https://www.example.com"


@pytest.fixture
def short_url():
    return ShortURL.objects.create(original=LONG_URL)


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


def test_retrieve_original_link_return_link(client, short_url):
    url = reverse(RETRIEVE_ORIGINAL_LINK_ENDPOINT, args=(short_url.token,))
    response = client.get(url)

    assert response.status_code == status.HTTP_302_FOUND
    assert response['Location'] == LONG_URL


def test_retrieve_original_link_return_404_when_link_not_exists(client):
    non_existing_token = "non-existing-token"
    assert not ShortURL.objects.filter(token=non_existing_token).exists()

    url = reverse(RETRIEVE_ORIGINAL_LINK_ENDPOINT, args=(non_existing_token,))
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_retrieve_original_link_log_clicks(client, short_url):
    assert short_url.click_count == 0
    assert short_url.clicks.count() == 0

    url = reverse(RETRIEVE_ORIGINAL_LINK_ENDPOINT, args=(short_url.token,))
    client.get(url)
    short_url.refresh_from_db()
    assert short_url.click_count == 1
    assert short_url.clicks.count() == 1

    client.get(url)
    short_url.refresh_from_db()
    assert short_url.click_count == 2
    assert short_url.clicks.count() == 2
