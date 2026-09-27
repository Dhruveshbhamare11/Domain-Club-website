from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
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
            "description": "Upload a photo file directly OR paste a direct image URL (Google Drive, Imgur, Discord, etc.). Uploaded photos are automatically compressed and saved permanently in the database."
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
        return mark_safe('<span style="color: #94a3b8; font-size: 11px;">No Photo</span>')

    photo_preview.short_description = "Avatar"

    def save_model(self, request, obj, form, change):
        # Read uploaded image directly from memory into a lightweight Base64 data URI
        # This completely avoids writing to the read-only /var/task filesystem on Vercel!
        photo_file = request.FILES.get("photo")
        if photo_file:
            try:
                from PIL import Image
                import base64
                import io

                img = Image.open(photo_file)
                if img.width > 400 or img.height > 400:
                    img.thumbnail((400, 400), Image.Resampling.LANCZOS)

                buffer = io.BytesIO()
                if img.mode in ("RGBA", "P"):
                    img.save(buffer, format="PNG", optimize=True)
                    mime = "image/png"
                else:
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    img.save(buffer, format="JPEG", quality=82, optimize=True)
                    mime = "image/jpeg"

                b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
                obj.photo_url = f"data:{mime};base64,{b64}"
                # Prevent writing to read-only disk on Vercel
                form.cleaned_data["photo"] = None
                obj.photo = ""
            except Exception:
                pass

        super().save_model(request, obj, form, change)


