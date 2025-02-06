from django.core.validators import URLValidator
from links.models import ShortURL
from rest_framework import serializers


class ShortURLSerializerV1(serializers.ModelSerializer):
    original = serializers.URLField(validators=[URLValidator()])

    class Meta:
        model = ShortURL
        fields = ["original"]


class StatisticsSerializerV1(serializers.ModelSerializer):
    ip_addresses = serializers.ReadOnlyField()
    user_agents = serializers.ReadOnlyField()

    class Meta:
        model = ShortURL
        fields = ["click_count", 'ip_addresses', 'user_agents']
