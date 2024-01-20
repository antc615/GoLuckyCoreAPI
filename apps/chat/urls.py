from django.urls import path
from .views import update_chat_analytics
from .views import get_user_chat_analytics

urlpatterns = [
    # ... other url patterns ...
    path('update-chat-analytics/', update_chat_analytics, name='update_chat_analytics'),
    path('user/<int:user_id>/', get_user_chat_analytics, name='user_chat_analytics'),
]