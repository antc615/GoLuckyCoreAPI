from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Like, Comment, Favorite
from .serializers import LikeSerializer, CommentSerializer, FavoriteSerializer
from apps.users.models import Image
from django.contrib.auth import get_user_model

User = get_user_model()

# Like views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_like(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if Like.objects.filter(user=request.user, image=image).exists():
        return Response({'message': 'Like already exists'}, status=status.HTTP_409_CONFLICT)

    like = Like.objects.create(user=request.user, image=image)
    return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_like(request, like_id):
    like = get_object_or_404(Like, id=like_id, user=request.user)
    like.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Comment views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, image=image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Favorite views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_favorite(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if Favorite.objects.filter(user=request.user, image=image).exists():
        return Response({'message': 'Favorite already exists'}, status=status.HTTP_409_CONFLICT)

    favorite = Favorite.objects.create(user=request.user, image=image)
    return Response(FavoriteSerializer(favorite).data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_favorite(request, favorite_id):
    favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
    favorite.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
