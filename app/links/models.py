from django.conf import settings
from django.db import models

MAX_TOKEN_LENGTH = 10


class ShortURL(models.Model):
    original = models.URLField(unique=True)
    token = models.CharField(max_length=MAX_TOKEN_LENGTH, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.BigIntegerField(default=0)

    def __str__(self):
        return self.token

    @property
    def url(self):
        return f"https://{settings.DOMAIN}/{self.token}"


class ClickLog(models.Model):
    short_url = models.ForeignKey(
        ShortURL, on_delete=models.CASCADE, related_name="clicks"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()

    def __str__(self):
        return f"Click on {self.short_url.url} from {self.ip_address}"
