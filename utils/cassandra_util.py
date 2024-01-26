# cassandra_util.py
from cassandra.cluster import Cluster
from cassandra.cluster import NoHostAvailable
from cassandra import ConsistencyLevel
from cassandra.policies import RetryPolicy
from django.conf import settings
from cassandra.util import uuid_from_time
import logging
import datetime

logger = logging.getLogger(__name__)

class CassandraConnection:
    _session = None

    @staticmethod
    def get_session():
        """
        Purpose: Establishes and reuses a single Cassandra session for the application.
        Usage: Called whenever a Cassandra session is needed, ensuring only one session is active. 
        It handles session creation and logs errors during connection attempts.
        """
        if CassandraConnection._session is None:
            try:
                # Create the Cluster instance with the custom retry policy
                cluster = Cluster(
                    settings.CASSANDRA_CLUSTER_NODES,
                    retry_policy=CustomRetryPolicy()
                )
                CassandraConnection._session = cluster.connect(settings.CASSANDRA_KEYSPACE)
                logger.info("Cassandra session created")
            except Exception as e:
                logger.error(f"Error connecting to Cassandra: {e}")
                raise e
        return CassandraConnection._session

def log_notification_event(recipient_id, sender_id, event_type, image_id=None, message=''):
    """
    Purpose: Logs a notification event to Cassandra.
    Usage: Called when an action occurs in the application that should trigger a notification, e.g., a user liking an image.
    Enhancement: Ensure the function uses the custom retry policy.
    """
    session = CassandraConnection.get_session()
    query = """
        INSERT INTO notification_events (event_id, recipient_id, sender_id, event_type, image_id, message, read, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, toUnixTimestamp(now()))
    """
    session.execute(query, (uuid_from_time(datetime.datetime.now()), recipient_id, sender_id, event_type, image_id, message, False))


def check_connection():
    """
    Purpose: Checks and maintains the health of the Cassandra session.
    Usage: Can be scheduled to run periodically to ensure the session is active. Attempts to reconnect if the session is down.
    """
    try:
        session = CassandraConnection.get_session()
        session.execute("SELECT * FROM system.local")
    except NoHostAvailable:
        CassandraConnection._session = None
        session = CassandraConnection.get_session()  # Attempt to reconnect


class CustomRetryPolicy(RetryPolicy):
    def on_read_timeout(self, query, consistency, required_responses,
                        received_responses, data_retrieved, retry_num):
        """
        Purpose: Defines custom behavior for retrying Cassandra read operations.
        Usage: Attached to the Cassandra cluster instance to automatically handle read timeouts.
        """
        # Decide when to retry, raise exception, or ignore based on your needs
        # Example: retry up to 3 times on a read timeout
        if retry_num < 3:
            return self.RETRY, consistency
        else:
            return self.RETHROW, None
