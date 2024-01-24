
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# from apps.notifications.services.notification_service import handle_like, handle_comment, handle_favorite

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_content(request, content_id):
    # handle_like(request.user.id, content_id)
    return Response({"message": "Content liked."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, content_id):
    comment_text = request.data.get("comment_text")
    # handle_comment(request.user.id, content_id, comment_text)
    return Response({"message": "Comment added."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def favorite_content(request, content_id):
    # handle_favorite(request.user.id, content_id)
    return Response({"message": "Content favorited."}, status=status.HTTP_200_OK)
