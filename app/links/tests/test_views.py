from django.urls import reverse
from links.models import ShortURL
from rest_framework import status

SHORT_URL_ENDPOINT_V1 = "v1:short-url"
LONG_URL = "https://www.example.com"


def test_create_short_url(client):
    body = {"original": LONG_URL}
    url = reverse(f'{SHORT_URL_ENDPOINT_V1}-list')
    response = client.post(url, body)

    expected_short_url = ShortURL.objects.get(original=LONG_URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["short_url"] == expected_short_url.url


def test_view_returns_short_url_if_exists(client):
    short_url = ShortURL.objects.create(original=LONG_URL)

    body = {"original": LONG_URL}
    url = reverse(f'{SHORT_URL_ENDPOINT_V1}-list')
    response = client.post(url, body)

    assert ShortURL.objects.filter(original=LONG_URL).count() == 1
    assert response.status_code == status.HTTP_200_OK
    assert response.data["short_url"] == short_url.url
