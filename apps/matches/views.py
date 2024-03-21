from django.shortcuts import render
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import Throttled
from django.core.cache import cache
from django.db import transaction
from django.db.models import Q
from .tasks import async_check_for_match

#Models
from .models import Match
from .serializers import MatchSerializer
from .models import Swipe
from .serializers import SwipeSerializer
from .models import Favorites
from .serializers import FavoritesSerializer
from .models import MatchFeedback
from .serializers import MatchFeedbackSerializer
from .models import CompatibilityScore
from .serializers import CompatibilityScoreSerializer
from .models import MatchRecommendation
from .serializers import MatchRecommendationSerializer
from .models import CompatibilityScore
from .serializers import CompatibilityScoreSerializer

#Services
from .services.matchmaking_service import MatchmakingService

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def match_list(request):
    if request.method == 'GET':
        user_matches = Match.objects.filter(user1=request.user) | Match.objects.filter(user2=request.user)
        # Pass the request in the context
        serializer = MatchSerializer(user_matches, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new match
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            # Additional validation or logic can be added here
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
# @ratelimit(key='user', rate='100/hour', method='POST', block=True)
def swipe_list_create(request):
    if request.method == 'GET':
        swipes = Swipe.objects.filter(swiper=request.user)
        serializer = SwipeSerializer(swipes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Rate Limiting (additional check if needed)
        # if request.limited:
        #     raise Throttled(detail='Too many swipe attempts. Try again later.')

        swiped_user_id = request.data.get('swiped')
        direction = request.data.get('direction')

        # Cache check for recent swipes to prevent database hit
        cache_key = f"{request.user.id}-{swiped_user_id}"
        if cache.get(cache_key):
            return Response({"error": "Please wait before swiping this user again."}, status=429)

        with transaction.atomic():
            # The rest of the validation and processing as before...
            if direction == "like":
                # Background task for match checking
                async_check_for_match.delay(request.user.id, swiped_user_id)
            
            # Set a short cache duration for this swipe to prevent rapid repeat swipes
            cache.set(cache_key, 'swiped', timeout=30)

        return Response(serializer.data, status=201) if serializer.is_valid() else Response(serializer.errors, status=400)

# Background task for checking matches
def check_for_match(swiper_id, swiped_user_id):
    if Swipe.objects.filter(swiper_id=swiped_user_id, swiped_id=swiper_id, direction="like").exists():
        Match.objects.create(user1_id=swiper_id, user2_id=swiped_user_id)
        # Trigger notifications or other events

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def favorites_list_create(request):
    if request.method == 'GET':
        favorites = Favorites.objects.filter(user=request.user)
        serializer = FavoritesSerializer(favorites, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Data validation can be added as needed
        serializer = FavoritesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def match_feedback_list_create(request):
    if request.method == 'GET':
        feedbacks = MatchFeedback.objects.filter(user=request.user)
        serializer = MatchFeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MatchFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Setting the user to the authenticated user
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def compatibility_score_list(request):
    if request.method == 'GET':
        scores = CompatibilityScore.objects.all()
        serializer = CompatibilityScoreSerializer(scores, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def compatibility_score_list_create(request):
    serializer = CompatibilityScoreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def match_recommendation_view(request):
    result = MatchmakingService.get_recommendations(request.user, request)
 
    if "error" in result:
        # If the service returned an error, respond with an appropriate message
        return Response({"message": result["error"]}, status=400)
    
    return Response({'recommendations': result})