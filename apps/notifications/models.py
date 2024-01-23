# apps/notifications/models.py

from django.db import models
from django.conf import settings

class Notification(models.Model):
    # Types of notifications
    LIKE = 'like'
    COMMENT = 'comment'
    FAVORITE = 'favorite'
    NOTIFICATION_TYPES = (
        (LIKE, 'Like'),
        (COMMENT, 'Comment'),
        (FAVORITE, 'Favorite'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, null=True)  # Additional content for the notification
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username} from {self.sender.username}"
