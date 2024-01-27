# interactions/tasks.py

from celery import shared_task
from utils.cassandra_util import log_notification_event
from apps.notifications.models import Notification  # Import the Notification model
import logging
from django.db import transaction

logger = logging.getLogger(__name__)

@shared_task
def async_log_notification_event(recipient_id, sender_id, event_type, image_id=None, message=''):
    """
    Logs a notification event to Cassandra and creates a notification in PostgreSQL.
    """
    try:

        with transaction.atomic():
            # Create PostgreSQL Notification
            Notification.objects.create(
                recipient_id=recipient_id,
                sender_id=sender_id,
                notification_type=event_type,
                image_id=image_id,
                message=message
            )
        log_notification_event(recipient_id, sender_id, event_type, image_id, message)
    except Exception as e:
        # Log the exception for debugging purposes
        logger.error(f"Failed to log notification event: {e}")
