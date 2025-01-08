from django.utils import timezone
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from celery import shared_task
from django.core.mail import send_mail


@shared_task(bind=True)
def send_email(self, subject, message, email):
    try:
        send_mail(
            subject,
            message,
            'noreply@testapp.com',
            [email],
            fail_silently=False,
        )
    except Exception as e:
        self.retry(exc=e, countdown=60)

# TODO: Uncomment this when we have a proper way to delete expired tokens
# @shared_task
# def cleanup_expired_tokens():
#     # Delete blacklisted tokens that have expired
#     BlacklistedToken.objects.filter(
#         token__expires_at__lt=timezone.now()
#     ).delete()

#     # Delete expired outstanding tokens
#     OutstandingToken.objects.filter(
#         expires_at__lt=timezone.now()
#     ).delete()
