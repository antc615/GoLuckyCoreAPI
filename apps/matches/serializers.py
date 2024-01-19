from rest_framework import serializers
from .models import Match
from .models import Swipe
from .models import Favorites

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