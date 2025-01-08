from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from ecommerce.settings import SITE_URL
from .tasks import send_email
import os


class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='app_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='app_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(
        default=uuid.uuid4, editable=False, null=True)

    picture = models.URLField(null=True, blank=True)

    password_reset_token = models.CharField(
        max_length=255, null=True, blank=True)
    password_reset_token_expiry = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def send_registration_email(self):
        subject = 'Welcome to our app'
        message = f'Thank you for registering. Please verify your email by clicking the link below: \n{
            SITE_URL}/api/auth/verify-email?token={self.email_verification_token}'
        return send_email.delay_on_commit(subject, message, self.email)

    def send_password_reset_email(self):
        subject = 'Password Reset Request'
        message = f'You are receiving this email because you requested a password reset for your account. Please click the link below to set a new password within 1 hour of receiving this email: \n{
            os.getenv("FRONTEND_RESET_PASSWORD_PAGE_URL")}?token={self.password_reset_token}'
        return send_email.delay_on_commit(subject, message, self.email)
