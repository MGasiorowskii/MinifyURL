from celery import shared_task
from core.redis import redis_client
from django.db import transaction
from links import base62, statistics
from links.models import ClickLog, ShortURL


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


@shared_task
def log_statistics(request_meta_data: dict, short_link_id: int):
    ip_address = statistics.get_client_ip(request_meta_data)
    user_agent = statistics.get_user_agent(request_meta_data)
    ClickLog.objects.create(
        short_url_id=short_link_id, ip_address=ip_address, user_agent=user_agent
    )
