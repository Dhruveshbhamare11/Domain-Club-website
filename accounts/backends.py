from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailOrUsernameBackend(ModelBackend):
    """Students sign in with email; username fallback keeps Django admin working."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = kwargs.get("email") or username
        if not identifier or not password:
            return None
        user = User.objects.filter(email__iexact=identifier).first()
        if user is None:
            user = User.objects.filter(username=identifier).first()
        return user if user and user.check_password(password) and self.user_can_authenticate(user) else None
