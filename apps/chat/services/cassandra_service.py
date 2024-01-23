from cassandra.cluster import Cluster
from cassandra.util import uuid_from_time

def save_message(sender_id, receiver_id, message_content):
    cluster = Cluster(['127.0.0.1'])  # Adjust as needed
    session = cluster.connect('golucky')

    query = """
    INSERT INTO chat_messages (message_id, sender_id, receiver_id, message_content, timestamp)
    VALUES (uuid(), %s, %s, %s, toTimeStamp(now()))
    """
    session.execute(query, (sender_id, receiver_id, message_content))
    

def get_chat_history(chat_id, limit=100):
    cluster = Cluster(['127.0.0.1'])  # Adjust as needed
    session = cluster.connect('golucky')

    query = "SELECT * FROM chat_messages WHERE chat_id = %s ORDER BY timestamp DESC LIMIT %s"
    rows = session.execute(query, (chat_id, limit))
    return rows
