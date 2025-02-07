import redis

from django.conf import settings

redis_client = redis.Redis().from_url(settings.REDIS_CACHE_URL)
