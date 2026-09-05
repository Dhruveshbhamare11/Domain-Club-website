from django.db import migrations


DEFAULT_BADGES = (
    ("FIRST_WIN", "Speed Demon", "Fastest correct solver of a puzzle.", "bolt"),
    ("STREAK_3", "On Fire", "Solve three puzzles correctly in a row.", "flame"),
    ("STREAK_5", "Unstoppable", "Solve five puzzles correctly in a row.", "rocket"),
    ("STREAK_10", "Mathematical Machine", "Solve ten puzzles correctly in a row.", "trophy"),
    ("MONTHLY_WINNER", "Math Champion", "Finish first in a completed monthly competition.", "crown"),
    ("PERFECT_MONTH", "Perfect Month", "Correctly solve every processed puzzle in a month.", "star"),
)


def seed_default_badges(apps, schema_editor):
    Badge = apps.get_model("badges", "Badge")
    for code, name, description, icon_name in DEFAULT_BADGES:
        Badge.objects.get_or_create(
            code=code,
            defaults={"name": name, "description": description, "icon_name": icon_name},
        )


def remove_seeded_badges(apps, schema_editor):
    Badge = apps.get_model("badges", "Badge")
    Badge.objects.filter(code__in=[badge[0] for badge in DEFAULT_BADGES]).delete()


class Migration(migrations.Migration):
    dependencies = [("badges", "0001_initial")]

    operations = [migrations.RunPython(seed_default_badges, remove_seeded_badges)]
