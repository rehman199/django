from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.exceptions import AuthenticationFailed


class VerifiedUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )

            if not user.email_verified:
                raise AuthenticationFailed(
                    'Please verify your email address before logging in.')

            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
