from core.redis import redis_client
from django.core.validators import URLValidator
from links.models import ShortURL
from rest_framework import serializers


class ShortenSerializerV1(serializers.ModelSerializer):
    original = serializers.URLField(validators=[URLValidator()])

    class Meta:
        model = ShortURL
        fields = ["original"]


class StatisticsSerializerV1(serializers.ModelSerializer):
    token = serializers.ReadOnlyField()
    click_count = serializers.SerializerMethodField()
    ip_addresses = serializers.SerializerMethodField()
    user_agents = serializers.SerializerMethodField()

    class Meta:
        model = ShortURL
        fields = ["token", "click_count", 'ip_addresses', 'user_agents']

    def get_click_count(self, obj):
        fresh_clicks = redis_client.get(f"clicks:{obj.token}") or 0
        return obj.click_count + int(fresh_clicks)

    def get_ip_addresses(self, obj):
        return [] if obj.ip_addresses == [None] else obj.ip_addresses

    def get_user_agents(self, obj):
        return [] if obj.user_agents == [None] else obj.user_agents
