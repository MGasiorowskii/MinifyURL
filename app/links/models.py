from django.db import models


class ShortURL(models.Model):
    original = models.URLField(unique=True)
    token = models.CharField(max_length=10, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.BigIntegerField(default=0)

    def __str__(self):
        return self.token
