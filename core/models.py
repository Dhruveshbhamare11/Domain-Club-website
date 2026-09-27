from django.db import models


class TeamMember(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    branch_year = models.CharField(max_length=150, blank=True)
    photo = models.ImageField(upload_to="team/", blank=True)
    photo_url = models.TextField(blank=True, help_text="Direct image URL or persistent auto-generated Data URI")
    bio = models.TextField(blank=True)
    social_link = models.URLField(blank=True)
    anime_quote = models.CharField(max_length=255, blank=True, help_text="Famous anime dialogue or quote")
    anime_character = models.CharField(max_length=100, blank=True, help_text="Companion Anime Character (e.g., Luffy, Gojo, Zoro, Naruto)")
    special_power = models.CharField(max_length=150, blank=True, help_text="e.g., Domain Expansion: Infinite Logic")
    bounty_or_power = models.CharField(max_length=100, blank=True, help_text="e.g., Power Level: 9000+ or Bounty: ฿1,500,000,000")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("order", "name")

    def __str__(self):
        return f"{self.name} ({self.role})"

    @property
    def avatar(self):
        """Returns the primary image: photo_url (Base64/direct link) or uploaded photo URL."""
        if self.photo_url:
            return self.photo_url
        if self.photo:
            try:
                return self.photo.url
            except Exception:
                return ""
        return ""

    def save(self, *args, **kwargs):
        # Auto-convert uploaded photo into a persistent Base64 Data URI
        # This guarantees photos never get lost when Vercel serverless containers restart.
        if self.photo and not self.photo_url:
            try:
                from PIL import Image
                import base64
                import io

                self.photo.open()
                img = Image.open(self.photo)

                # Resize to max 400x400 to keep DB storage ultra-lightweight (< 30KB)
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
                self.photo_url = f"data:{mime};base64,{b64}"
            except Exception:
                pass

        super().save(*args, **kwargs)

        # Invalidate in-memory caches immediately so updates reflect on the website
        from django.core.cache import cache
        cache.delete("team_all_members")
        cache.delete("home_page_data")

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        from django.core.cache import cache
        cache.delete("team_all_members")
        cache.delete("home_page_data")

