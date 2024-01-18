#DRF
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

#MODELS
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .models import UserPreferences
from .serializers import UserPreferencesSerializer

#AUTH
from django.contrib.auth import get_user_model, authenticate
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

#EMAIL
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.urls import reverse

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)  # Debugging statement
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)  # partial=True for PATCH
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile(request):
    user = request.user
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not authenticate(username=user.username, password=old_password):
        return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)

    # Add additional password validation here if needed

    user.password = make_password(new_password)
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def request_reset_password(request):
    UserModel = get_user_model()  # Get the custom user model
    email = request.data.get('email')
    try:
        user = UserModel.objects.get(email=email)
        token = PasswordResetTokenGenerator().make_token(user)
        reset_link = request.build_absolute_uri(reverse('password_reset_confirm')) + '?token=' + token
        send_mail(
            'Password Reset Request',
            'Here is your password reset link: ' + reset_link,
            'antc615@gmail.com',
            [email],
            fail_silently=False,
        )
        return Response(status=status.HTTP_200_OK)
    except User.DoesNotExist:
        # Do not reveal that the email does not exist for security reasons
        return Response(status=status.HTTP_200_OK)
    

@api_view(['POST'])
def password_reset_confirm(request):
    UserModel = get_user_model()
    token = request.data.get('token')
    password = request.data.get('password')

    # Token validation
    for user in UserModel.objects.all():
        if PasswordResetTokenGenerator().check_token(user, token):
            # Password update
            user.set_password(password)
            user.save()
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)

    # Invalid token
    return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deactivate_account(request):
    user = request.user
    user.is_active = False
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow requests regardless of user state
def reactivate_account(request):
    UserModel = get_user_model()
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate the user
    user = authenticate(username=username, password=password, reactivating=True)
    if user and not user.is_active:
        # Reactivate the user account
        user.is_active = True
        user.save()
        return Response({"message": "Account reactivated successfully."}, status=status.HTTP_200_OK)

    return Response({"error": "Invalid credentials or account already active."}, status=status.HTTP_400_BAD_REQUEST)

## USER PREFERENCES ##################################################
@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_preferences(request):
    user = request.user
    user_preferences, created = UserPreferences.objects.get_or_create(user=user)

    if request.method == 'GET':
        serializer = UserPreferencesSerializer(user_preferences)
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        serializer = UserPreferencesSerializer(user_preferences, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)