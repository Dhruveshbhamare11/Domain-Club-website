from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import StudentProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.get_or_create(user=instance, defaults={"branch": "COMPS", "year": "FE"})
    cache.delete("home_page_data")
    cache.delete("all_time_profiles_data")


@receiver(post_delete, sender=User)
def clear_caches_on_user_delete(sender, instance, **kwargs):
    cache.delete("home_page_data")
    cache.delete("all_time_profiles_data")

