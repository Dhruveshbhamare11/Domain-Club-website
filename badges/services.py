from .models import Badge, UserBadge


def award_badge(user, code):
    badge = Badge.objects.filter(code=code).first()
    return UserBadge.objects.get_or_create(user=user, badge=badge)[0] if badge else None


def award_streak_badges(user):
    streak = user.profile.current_streak
    for threshold, code in ((3, "STREAK_3"), (5, "STREAK_5"), (10, "STREAK_10")):
        if streak >= threshold:
            award_badge(user, code)
