from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ChatAnalytics
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

@api_view(['POST'])
def update_chat_analytics(request):
    # Example payload: {"user_id": 1, "total_messages_sent": 5, ...}
    User = get_user_model()
    user_id = request.data.get('user_id')
    total_messages_sent = request.data.get('total_messages_sent')
    total_messages_received = request.data.get('total_messages_received')
    average_response_time = request.data.get('average_response_time')
    conversation_starts = request.data.get('conversation_starts')
    conversation_depth = request.data.get('conversation_depth')

    user = User.objects.get(pk=user_id)
    analytics, created = ChatAnalytics.objects.get_or_create(user=user)

    analytics.total_messages_sent += total_messages_sent
    analytics.total_messages_received += total_messages_received
    analytics.average_response_time = average_response_time
    analytics.conversation_starts += conversation_starts
    analytics.conversation_depth = max(analytics.conversation_depth, conversation_depth)
    analytics.save()

    return Response({"status": "success", "data": {"user": user.username, "analytics": analytics.id}})

def get_user_chat_analytics(request, user_id):
    # Assuming you're passing the user_id as an argument
    analytics = get_object_or_404(ChatAnalytics, user_id=user_id)
    
    data = {
        "total_messages_sent": analytics.total_messages_sent,
        "total_messages_received": analytics.total_messages_received,
        "average_response_time": analytics.average_response_time,
        "conversation_starts": analytics.conversation_starts,
        "conversation_depth": analytics.conversation_depth,
        "last_updated": analytics.last_updated
    }

    return JsonResponse(data)