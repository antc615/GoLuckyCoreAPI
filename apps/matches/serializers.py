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
    match_details = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = ['id', 'match_details', 'matched_on', 'is_active']

    def get_match_details(self, obj):
        request = self.context.get('request')
        # Determine which user is the match (not the requester) and serialize their details
        if obj.user1 == request.user:
            match_user = obj.user2
        else:
            match_user = obj.user1
        return UserWithImageSerializer(match_user, context={'request': request}).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Modify to_representation to use 'match_details' instead of 'user1_details' and 'user2_details'
        request = self.context.get('request')
        if instance.user1 == request.user:
            match_user_details = UserWithImageSerializer(instance.user2, context={'request': request}).data
        else:
            match_user_details = UserWithImageSerializer(instance.user1, context={'request': request}).data
        # Remove user1_details and user2_details from the representation
        representation.pop('user1_details', None)
        representation.pop('user2_details', None)
        # Add match_user_details under a suitable key, for example 'match_details'
        representation['match_details'] = match_user_details
        return representation
    
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
        read_only_fields = ['swiper']  # Ensure swiper is not writable directly

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