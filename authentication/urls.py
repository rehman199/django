from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,)
from .views import (register, current_user, request_password_reset,
                    reset_password, verify_password_reset, verify_email, logout)

urlpatterns = [
    path('register', register, name='register'),
    path('login', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email', verify_email, name='verify_email'),
    path('me', current_user, name='current_user'),
    path('logout', logout, name='logout'),
    path('reset-password', request_password_reset,
         name='request_password_reset'),
    path('reset-password/verify', verify_password_reset,
         name='verify_password_reset'),
    path('reset-password/submit', reset_password, name='reset_password'),
]
