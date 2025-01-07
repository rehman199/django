from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,)
from .views import register, current_user

urlpatterns = [
    path('register', register, name='register'),
    path('login', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('me', current_user, name='current_user'),
]
