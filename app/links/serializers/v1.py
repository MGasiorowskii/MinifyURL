from django.core.validators import URLValidator
from links.models import ShortURL
from rest_framework import serializers


class ShortenSerializerV1(serializers.ModelSerializer):
    original = serializers.URLField(validators=[URLValidator()])

    class Meta:
        model = ShortURL
        fields = ["original"]


class StatisticsSerializerV1(serializers.ModelSerializer):
    ip_addresses = serializers.SerializerMethodField()
    user_agents = serializers.SerializerMethodField()

    class Meta:
        model = ShortURL
        fields = ["click_count", 'ip_addresses', 'user_agents']

    def get_ip_addresses(self, obj):
        return [] if obj.ip_addresses == [None] else obj.ip_addresses

    def get_user_agents(self, obj):
        return [] if obj.user_agents == [None] else obj.user_agents
