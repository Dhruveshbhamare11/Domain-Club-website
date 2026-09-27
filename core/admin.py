from django.contrib import admin
from django.utils.html import format_html
from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "branch_year", "order", "photo_preview")
    list_editable = ("role", "branch_year", "order")
    search_fields = ("name", "role", "branch_year", "anime_character")
    list_filter = ("branch_year",)
    ordering = ("order", "name")
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "role", "branch_year", "order")
        }),
        ("Photo / Avatar", {
            "fields": ("photo", "photo_url"),
            "description": "Upload a photo file directly OR paste a direct image URL (Google Drive, Imgur, Discord, etc.). Uploaded photos are automatically compressed and saved permanently."
        }),
        ("Anime / Guild Identity", {
            "fields": ("anime_character", "anime_quote", "special_power", "bounty_or_power")
        }),
        ("Biography & Socials", {
            "fields": ("bio", "social_link")
        }),
    )

    def photo_preview(self, obj):
        url = obj.avatar
        if url:
            return format_html(
                '<img src="{}" style="width: 36px; height: 36px; border-radius: 50%; object-fit: cover; border: 2px solid #e2e8f0; vertical-align: middle;" />',
                url
            )
        return format_html('<span style="color: #94a3b8; font-size: 11px;">No Photo</span>')

    photo_preview.short_description = "Avatar"

