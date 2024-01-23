from django.urls import path
from .views import update_chat_analytics
from .views import get_user_chat_analytics
from .views import chat_history_view

urlpatterns = [
    path('update-chat-analytics/', update_chat_analytics, name='update_chat_analytics'),
    path('user/<int:user_id>/', get_user_chat_analytics, name='user_chat_analytics'),    
    path('history/<str:other_user_id>/', chat_history_view, name='chat_history'),
]