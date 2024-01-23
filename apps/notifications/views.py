# apps/notifications/views.py

from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # Filter notifications for the logged-in user
        user = self.request.user
        return user.notifications.all()  # This will show all notifications for the user
