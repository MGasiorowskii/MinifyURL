from celery import shared_task
from core.redis import redis_client
from django.db import transaction
from links import base62
from links.models import ShortURL


@shared_task
def sync_clicks_to_db():
    to_update = []
    with transaction.atomic():
        for key in redis_client.keys("clicks:*"):
            token = key.decode().split(":")[1]
            count = int(redis_client.get(key))
            short_url = ShortURL.objects.get(id=base62.decode(token))
            short_url.click_count += count
            to_update.append(short_url)
            redis_client.delete(key)

        ShortURL.objects.bulk_update(to_update, ["click_count"])
