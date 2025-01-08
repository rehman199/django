from rest_framework_simplejwt.tokens import TokenError, RefreshToken
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
import uuid
from django.utils import timezone
from django.shortcuts import redirect
import os


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data['user'])

    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['user']['password'])
        user.save()
        user.send_registration_email()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def verify_email(request):
    user = User.objects.filter(
        email_verification_token=request.query_params['token']).first()

    if user is None:
        return redirect(os.getenv('FRONTEND_LOGIN_PAGE_URL') + '?error=No user found with this token')

    user.email_verified = True
    user.email_verification_token = None
    user.save()

    return redirect(os.getenv('FRONTEND_LOGIN_PAGE_URL') + '?success=Email verified successfully')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except TokenError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def request_password_reset(request):
    user = User.objects.get(email=request.data['email'])

    if (user is None):
        return Response({'error': 'No user found with this email'}, status=status.HTTP_404_NOT_FOUND)

    user.password_reset_token = uuid.uuid4()
    user.password_reset_token_expiry = timezone.now() + timezone.timedelta(hours=1)
    user.save()
    user.send_password_reset_email()

    return Response({'message': 'Password reset instructions (which will expire in 1 hour) are sent to your email.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def verify_password_reset(request):
    user = User.objects.get(password_reset_token=request.query_params['token'])

    if (user is None):
        return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Token is valid', 'email': user.email}, status=status.HTTP_200_OK)


@api_view(['POST'])
def reset_password(request):
    user = User.objects.filter(
        password_reset_token=request.data['token'], password_reset_token_expiry__gte=timezone.now()).first()

    if (user is None):
        return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(request.data['password'])
    user.password_reset_token = None
    user.password_reset_token_expiry = None
    user.save()

    return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
