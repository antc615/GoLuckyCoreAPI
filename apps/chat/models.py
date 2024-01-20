from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatAnalytics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_messages_sent = models.IntegerField(default=0)
    total_messages_received = models.IntegerField(default=0)
    average_response_time = models.FloatField(default=0.0)  # In seconds
    conversation_starts = models.IntegerField(default=0)
    conversation_depth = models.IntegerField(default=0)  # Measured in number of messages
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.user.username}"