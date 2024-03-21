from rest_framework import serializers
from .models import Match
from .models import Swipe
from .models import Favorites
from .models import MatchFeedback
from .models import CompatibilityScore
from .models import MatchRecommendation
from django.contrib.auth import get_user_model
from .models import User
from apps.users.models import Image, UserProfile
from apps.users.serializers import ImageSerializer

#Services
from .services.matchmaking_service import get_random_user_image_url

User = get_user_model()

class MatchSerializer(serializers.ModelSerializer):
    user1_details = serializers.SerializerMethodField()
    user2_details = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = '__all__'

    def get_user1_details(self, obj):
        # This method is now just a placeholder, actual implementation happens in to_representation
        pass

    def get_user2_details(self, obj):
        # This method is now just a placeholder, actual implementation happens in to_representation
        pass

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        ret['user1_details'] = UserWithImageSerializer(instance.user1, context={'request': request}).data
        ret['user2_details'] = UserWithImageSerializer(instance.user2, context={'request': request}).data
        return ret
    
class UserWithImageSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'images']

    def get_images(self, obj):
        user_profile = UserProfile.objects.filter(user=obj).first()
        if not user_profile:
            return []
        images = Image.objects.filter(user_profile=user_profile)
        return ImageSerializer(images, many=True, context=self.context).data

        
class SwipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swipe
        fields = '__all__'
        extra_kwargs = {
            'swiper': {'read_only': True}
        }

class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'timestamp': {'read_only': True}
        }

class MatchFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchFeedback
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }

class CompatibilityScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompatibilityScore
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }

class MatchRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchRecommendation
        fields = '__all__'