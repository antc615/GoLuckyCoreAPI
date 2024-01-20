from rest_framework import serializers
from .models import Match
from .models import Swipe
from .models import Favorites
from .models import MatchFeedback
from .models import CompatibilityScore
from .models import MatchRecommendation


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'
        
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