from django.core.validators import URLValidator
from links.models import ShortURL
from rest_framework import serializers


class ShortURLSerializer(serializers.ModelSerializer):
    original = serializers.URLField(validators=[URLValidator()])

    class Meta:
        model = ShortURL
        fields = ["original"]
