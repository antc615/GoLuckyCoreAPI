#DRF
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

#MODELS
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .models import UserPreferences
from .serializers import UserPreferencesSerializer
from .models import UserProfile
from .serializers import UserProfileSerializer
from .models import Image
from .serializers import ImageSerializer
from django.db.models import Q

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

#MEDIA
from utils.media_util import build_absolute_image_url

@api_view(['POST'])
@permission_classes([AllowAny])
def refreshToken(request):
    refresh_token = request.data.get('refresh')
    if refresh_token is None:
        return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Attempt to create a new token using the provided refresh token
        token = RefreshToken(refresh_token)
        # Get the user based on the token
        user_id = token['user_id']
        UserModel = get_user_model()
        user = UserModel.objects.get(id=user_id)

        # Generate a new access token
        new_access_token = str(token.access_token)

        # Rotate the refresh token to a new one (for added security)
        token.blacklist()  # Ensure blacklisting is configured if you use this
        new_refresh_token = str(RefreshToken.for_user(user))

        return Response({
            'access': new_access_token,
            'refresh': new_refresh_token,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle invalid or expired refresh token
        print(e)  # Debugging: print or log the exception message
        return Response({"error": "Invalid or expired refresh token."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)  # Debugging statement
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def registerLogin(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user = authenticate(username=user.username, password=request.data['password'])
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Authentication failed after registration."}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def user_profile(request):
#     user = request.user
#     serializer = UserSerializer(user)
#     return Response(serializer.data)

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

########################## USER PROFILE ##########################
@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user, defaults={
        'profile_picture': '../assets/default_profile.jpg',
        'biography': '',
        'location': 'Unknown',
        'hobbies': '',
        'education': '',
        'occupation': 'Not specified',
        'relationship_status': 'Not specified',
        'height': 'Not specified',
        'looking_for': 'Not specified',
    })

    if request.method == 'GET':
        profile_data = UserProfileSerializer(profile).data
        # Manually add absolute URL for profile picture
        profile_data['profile_picture'] = build_absolute_image_url(request, profile.profile_picture)
        
        # Inside your GET request handling in user_profile view
        images_queryset = profile.images.exclude(Q(image='') | Q(image=None))
        images_data = []
        for image in images_queryset:
            image_url = build_absolute_image_url(request, image.image)
            if image_url:  # This check ensures only images with a valid URL are processed
                images_data.append({
                    'id': image.id,
                    'url': image_url,
                    'uploaded_at': image.uploaded_at,
                    'description': image.description,
                    'is_profile_picture': image.is_profile_picture,
                })
        profile_data['images'] = images_data
        return Response(profile_data)
    
    elif request.method in ['PUT', 'PATCH']:
        serializer = UserProfileSerializer(profile, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
### IMAGES
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image_authenticated(request):
    print(request.FILES)  # Debugging: Check if the 'file' is in the request

    # No need to get user_id from URL, use request.user directly
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user, defaults={
        'profile_picture': '../assets/default_profile.jpg',
        'biography': '',
        'location': 'Unknown',
        'hobbies': '',
        'education': '',
        'occupation': 'Not specified',
        'relationship_status': 'Not specified',
        'height': 'Not specified',
        'looking_for': 'Not specified',
    })
    
    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save(user_profile=request.user.profile)
        file = request.FILES.get('file')  # Ensure this key matches your frontend
        if file:
            instance.image = file
            instance.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request, user_id):
    User = get_user_model()  # Get the custom user model
    try:
        user = User.objects.get(id=user_id)
        if request.user != user:
            return Response({"message": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)
        profile, created = UserProfile.objects.get_or_create(user=user, defaults={
        'profile_picture': '../assets/default_profile.jpg',
        'biography': '',
        'location': 'Unknown',
        'hobbies': '',
        'education': '',
        'occupation': 'Not specified',
        'relationship_status': 'Not specified',
        'height': 'Not specified',
        'looking_for': 'Not specified',
    })
    except User.DoesNotExist:
        return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        # Use 'profile' variable here instead of 'user_profile'
        serializer.save(user_profile=profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_image(request, user_id, image_id):
    User = get_user_model()  # Get the custom user model
    try:
        user = User.objects.get(id=user_id)
        if request.user != user:
            return Response({"message": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

        # Ensure the image belongs to the user's profile
        image = Image.objects.get(id=image_id, user_profile__user=user)
    except User.DoesNotExist:
        return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Image.DoesNotExist:
        return Response({"message": "Image not found."}, status=status.HTTP_404_NOT_FOUND)

    image.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_image_inactive(request, user_id, image_id):
    User = get_user_model()  # Get the custom user model
    try:
        user = User.objects.get(id=user_id)
        if request.user != user:
            return Response({"message": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

        # Ensure the image belongs to the user's profile
        image = Image.objects.get(id=image_id, user_profile__user=user)
        # Mark the image as inactive instead of deleting
        image.active = False
        image.save()
        return Response({"message": "Image marked as inactive successfully."}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Image.DoesNotExist:
        return Response({"message": "Image not found."}, status=status.HTTP_404_NOT_FOUND)