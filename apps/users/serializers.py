# serializers.py
from .models import User
from .models import UserPreferences
from .models import UserProfile
from .models import Image

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = '__all__'
        read_only_fields = ('user',)

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'uploaded_at', 'description', 'is_profile_picture', 'active']

class UserProfileSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'user', 'profile_picture', 'biography', 'age', 'location', 'hobbies',
            'education', 'occupation', 'relationship_status', 'height', 'looking_for',
            'images', 'phone_number'
        ]