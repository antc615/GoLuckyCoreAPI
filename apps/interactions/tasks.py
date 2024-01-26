# interactions/tasks.py

from celery import shared_task
from utils.cassandra_util import log_notification_event  # Updated import statement

@shared_task
def async_log_notification_event(recipient_id, sender_id, event_type, image_id=None, message=''):
    """
    Asynchronously logs a notification event to Cassandra.
    This Celery task abstracts the asynchronous execution of event logging.
    """
    log_notification_event(recipient_id, sender_id, event_type, image_id, message)
