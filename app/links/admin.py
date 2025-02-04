from django.contrib import admin
from links.models import ShortURL


@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ("original", "token", "created_at", "click_count")
    search_fields = ("token", "original")
    list_filter = ("created_at",)
    date_hierarchy = "created_at"
    ordering = ("created_at",)
    readonly_fields = ("created_at", "click_count")
    fields = ("original", "token", "created_at", "click_count")
    actions = ["reset_click_count"]

    def reset_click_count(self, request, queryset):
        queryset.update(click_count=0)

    reset_click_count.short_description = "Reset Click Count"
