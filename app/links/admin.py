from django.contrib import admin
from links.models import ClickLog, ShortURL


@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ("original", "token", "created_at", "click_count")
    search_fields = ("token", "original")
    list_filter = ("created_at",)
    date_hierarchy = "created_at"
    ordering = ("created_at",)
    readonly_fields = ("created_at", "click_count")
    actions = ["reset_click_count"]

    def reset_click_count(self, request, queryset):
        queryset.update(click_count=0)

    reset_click_count.short_description = "Reset Click Count"


@admin.register(ClickLog)
class ClickLogAdmin(admin.ModelAdmin):
    list_display = ('short_url', 'timestamp', 'ip_address', 'user_agent')
    list_filter = ("timestamp",)
    date_hierarchy = 'timestamp'
    ordering = ("timestamp",)
    readonly_fields = ("timestamp",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('short_url')
