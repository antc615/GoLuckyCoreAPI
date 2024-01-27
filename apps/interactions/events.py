# interactions/events.py
from .tasks import async_log_notification_event

def log_like_event(user, image):
    """
    Log a 'like' notification event to Cassandra.
    This function abstracts the logging details for a like event.
    """
    async_log_notification_event.delay(
        recipient_id=image.user_profile.user.id,  # Accessing the user_id through the user_profile
        sender_id=user.id,
        event_type='like',
        image_id=image.id,
        message=f'{user.username} liked your image'
    )
