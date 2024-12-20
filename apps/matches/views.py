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
from django.db.models import Count
from apps.users.models import Image, UserProfile

#Services
from .services.matchmaking_service import MatchmakingService
from .services.match_service import MatchFilteringService

#Database
from django.db import IntegrityError

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def match_list(request):
    if request.method == 'GET':
        filtered_matches = MatchFilteringService.filter_matches_with_images(request.user)
        
        # Serialize and return the filtered matches
        serializer = MatchSerializer(filtered_matches, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        # Handle match creation logic here
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def swipe_list_create(request):
    if request.method == 'GET':
        swipes = Swipe.objects.filter(swiper=request.user)
        serializer = SwipeSerializer(swipes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['swiper'] = request.user.id

        # Preliminary check for existing like in the same direction
        swiped_id = int(data.get('swiped'))
        existing_like = Swipe.objects.filter(swiper_id=request.user.id, swiped_id=swiped_id, direction="like").first()

        if existing_like:
            # Optionally, for testing, acknowledge the like without creating a duplicate
            return Response({"message": "Like already exists, not duplicated for testing purposes."}, status=200)

        serializer = SwipeSerializer(data=data)
        # Cache check for recent swipes to prevent rapid repeat
        cache_key = f"{request.user.id}-{data.get('swiped')}"
        if cache.get(cache_key):
            return Response({"error": "Please wait before swiping this user again."}, status=429)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    # For testing: Delete previous like if exists
                    Swipe.objects.filter(
                        swiper_id=request.user.id,
                        swiped_id=data.get('swiped'),
                        direction="like"
                    ).delete()

                    serializer.save(swiper=request.user)

                    # Check for a match if the direction is "like"
                    match_result = False
                    if data.get('direction') == "like":
                        swiped_user_id = data.get('swiped')
                        Swipe.objects.create(swiper_id=swiped_user_id, swiped_id=request.user.id, direction="like")

                        # Background task for match checking (assuming this is correctly set up elsewhere)
                        async_check_for_match.delay(request.user.id, data.get('swiped'))

                        # Check for and persist match
                        match_result = check_for_match(request.user.id, data.get('swiped'))

                    # Set a short cache duration for this swipe
                    cache.set(cache_key, 'swiped', timeout=30)

                    response_data = serializer.data
                    response_data['match_created'] = match_result

                    # For testing: Optionally delete the like after creation for repeated testing
                    Swipe.objects.filter(
                        swiper_id=request.user.id,
                        swiped_id=data.get('swiped'),
                        direction="like"
                    ).delete()

                    return Response(response_data, status=201)
            except IntegrityError as e:
                return Response({"error": str(e)}, status=400)
        else:
            return Response(serializer.errors, status=400)

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def match_list(request):
#     if request.method == 'GET':
#         user_matches = Match.objects.filter(Q(user1=request.user) | Q(user2=request.user))

#         # Initialize an empty list to hold matches where both users have at least one image
#         filtered_matches = []

#         for match in user_matches:
#             # Check for the existence of UserProfiles for both users
#             user1_profile_exists = UserProfile.objects.filter(user=match.user1).exists()
#             user2_profile_exists = UserProfile.objects.filter(user=match.user2).exists()

#             if user1_profile_exists and user2_profile_exists:
#                 user1_profile = UserProfile.objects.get(user=match.user1)
#                 user2_profile = UserProfile.objects.get(user=match.user2)

#                 user1_images_exists = user1_profile.images.exclude(Q(image='') | Q(image=None)).filter(active=True).exists()
#                 user2_images_exists = user2_profile.images.exclude(Q(image='') | Q(image=None)).filter(active=True).exists()

#                 # Only include the match if both users have at least one active image
#                 if user1_images_exists and user2_images_exists:
#                     filtered_matches.append(match)
        
#         # Serialize and return the filtered matches
#         serializer = MatchSerializer(filtered_matches, many=True, context={'request': request})
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         # Create a new match
#         serializer = MatchSerializer(data=request.data)
#         if serializer.is_valid():
#             # Additional validation or logic can be added here
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# # @ratelimit(key='user', rate='100/hour', method='POST', block=True)
# def swipe_list_create(request):
#     if request.method == 'GET':
#         swipes = Swipe.objects.filter(swiper=request.user)
#         serializer = SwipeSerializer(swipes, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         # Rate Limiting (additional check if needed)
#         # if request.limited:
#         #     raise Throttled(detail='Too many swipe attempts. Try again later.')

#         # Include the current user's ID in the data to be serialized
#         data = request.data.copy()  # Make a mutable copy of the request data
#         data['swiper'] = request.user.id  # Set the swiper to the current user

#         serializer = SwipeSerializer(data=data)  # Initialize the serializer with the modified data

#         # Cache check for recent swipes to prevent database hit
#         cache_key = f"{request.user.id}-{data.get('swiped')}"
#         if cache.get(cache_key):
#             return Response({"error": "Please wait before swiping this user again."}, status=429)

#         if serializer.is_valid():
#             with transaction.atomic():
#                  # Directly pass the swiper to the save method
#                 serializer.save(swiper=request.user)

#                 # Check for a match if the direction is "like"
#                 if data.get('direction') == "like":
#                     swiped_user_id = data.get('swiped')
#                     if not Swipe.objects.filter(swiper_id=swiped_user_id, swiped_id=request.user.id).exists():
#                         Swipe.objects.create(swiper_id=swiped_user_id, swiped_id=request.user.id, direction="like")
                    
#                     # Background task for match checking
#                     async_check_for_match.delay(request.user.id, data.get('swiped'))
                    
#                     # Persist match if exist
#                     match_result = check_for_match(request.user.id, data.get('swiped'))

#                 # Set a short cache duration for this swipe to prevent rapid repeat swipes
#                 cache.set(cache_key, 'swiped', timeout=30)

#                 response_data = serializer.data
#                 response_data['match_created'] = match_result
#             return Response(serializer.data, status=201)
#         else:
#             return Response(serializer.errors, status=400)
        
def check_for_match(swiper_id, swiped_user_id):
    match_created = False  # Initialize the flag to False

    # Existing logic to check and create a match
    if Swipe.objects.filter(swiper_id=swiped_user_id, swiped_id=swiper_id, direction="like").exists():
        match_exists = Match.objects.filter(user1_id=swiper_id, user2_id=swiped_user_id).exists() or \
                       Match.objects.filter(user1_id=swiped_user_id, user2_id=swiper_id).exists()

        if not match_exists:
            Match.objects.create(user1_id=swiper_id, user2_id=swiped_user_id)
            match_created = True  # Set to True if a new match is created

            # Trigger notifications or other events here

    return match_created

# Background task for checking matches
def check_for_match_notifs(swiper_id, swiped_user_id):
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