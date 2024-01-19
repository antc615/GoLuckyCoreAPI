from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

#Models
from .models import Match
from .serializers import MatchSerializer
from .models import Swipe
from .serializers import SwipeSerializer
from .models import Favorites
from .serializers import FavoritesSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def match_list(request):
    if request.method == 'GET':
        # Filter matches relevant to the authenticated user
        user_matches = Match.objects.filter(user1=request.user) | Match.objects.filter(user2=request.user)
        serializer = MatchSerializer(user_matches, many=True)
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
def swipe_list_create(request):
    if request.method == 'GET':
        # Fetch and return the authenticated user's swipes
        swipes = Swipe.objects.filter(swiper=request.user)
        serializer = SwipeSerializer(swipes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new swipe with the authenticated user as the swiper
        serializer = SwipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(swiper=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

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