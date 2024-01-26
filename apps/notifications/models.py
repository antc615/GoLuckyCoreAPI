from django.db import models
from django.contrib.auth import get_user_model
from apps.users.models import Image

User = get_user_model()

class Notification(models.Model):
    # Define different types of notifications that can occur
    LIKE = 'like'
    COMMENT = 'comment'
    FAVORITE = 'favorite'
    MESSAGE = 'message'
    GAME_REQUEST = 'game_request'
    
    NOTIFICATION_TYPES = [
        (LIKE, 'Like'),
        (COMMENT, 'Comment'),
        (FAVORITE, 'Favorite'),
        (MESSAGE, 'Message'),
        (GAME_REQUEST, 'Game Request'),
    ]

    # Notification fields
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)  # For image-related notifications
    message = models.TextField()  # A short description of the notification
    read = models.BooleanField(default=False)  # Whether the notification has been read
    timestamp = models.DateTimeField(auto_now_add=True)

    # Optional: Link to the chat message or game request if needed
    # chat_message = models.ForeignKey('chat.Message', on_delete=models.CASCADE, null=True, blank=True)
    # game_request = models.ForeignKey('games.GameRequest', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']  # Most recent notifications first
        indexes = [
            models.Index(fields=['-timestamp']),  # Improve query performance for recent notifications
            models.Index(fields=['recipient', 'read']),  # Efficiently filter by user and read status
        ]

    def __str__(self):
        return f"Notification for {self.recipient.username} - {self.get_notification_type_display()}"

    @property
    def content_object(self):
        # Returns the associated object (image, chat message, etc.) based on the notification type
        if self.notification_type == self.LIKE or self.notification_type == self.COMMENT or self.notification_type == self.FAVORITE:
            return self.image
        # Uncomment and expand these as you implement the corresponding features
        # elif self.notification_type == self.MESSAGE:
        #     return self.chat_message
        # elif self.notification_type == self.GAME_REQUEST:
        #     return self.game_request
        return None