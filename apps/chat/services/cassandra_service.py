from cassandra.cluster import Cluster

def save_message(sender_id, receiver_id, message_content):
    cluster = Cluster(['127.0.0.1'])  # Adjust as needed
    session = cluster.connect('goluckly')

    query = """
    INSERT INTO chat_messages (message_id, sender_id, receiver_id, message_content, timestamp)
    VALUES (uuid(), %s, %s, %s, toTimeStamp(now()))
    """
    session.execute(query, (sender_id, receiver_id, message_content))
