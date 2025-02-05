from django.db.models.signals import post_save
from django.dispatch import receiver
from links.generator import generate_token
from links.models import ShortURL


@receiver(post_save, sender=ShortURL)
def create_token(sender, instance, **kwargs):
    if not instance.token:
        while True:
            token = generate_token(instance.id)
            if not ShortURL.objects.filter(token=token).exists():
                break

        instance.token = token
        instance.save(update_fields=['token'])
