from core.redis import redis_client
from django.contrib import admin
from links.models import ClickLog, ShortURL


@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = (
        "original",
        "token",
        "created_at",
        "click_count",
        'calculated_click_count',
        'url',
    )
    search_fields = ("token", "original")
    list_filter = ("created_at",)
    date_hierarchy = "created_at"
    ordering = ("created_at",)
    readonly_fields = ("created_at", "click_count")

    def calculated_click_count(self, obj):
        fresh_clicks = redis_client.get(f"clicks:{obj.token}") or 0
        return obj.click_count + int(fresh_clicks)

    calculated_click_count.short_description = "Calculated Click Count"


@admin.register(ClickLog)
class ClickLogAdmin(admin.ModelAdmin):
    list_display = ('short_url', 'timestamp', 'ip_address', 'user_agent')
    list_filter = ("timestamp",)
    date_hierarchy = 'timestamp'
    ordering = ("timestamp",)
    readonly_fields = ("timestamp",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('short_url')
