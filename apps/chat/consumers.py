import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .services.cassandra_service import save_message
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings

from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer

# Get the user model
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    """
    A WebSocket consumer that handles real-time chat functionality.

    This consumer manages WebSocket connections for chat sessions between users, 
    authenticates users via JWT tokens, handles incoming chat messages, saves messages 
    to a Cassandra database, and broadcasts messages to the appropriate recipients.

    Methods:
        connect: Establishes the WebSocket connection, authenticates the user, 
                 joins the chat room group.
        disconnect: Leaves the chat room group and closes the WebSocket connection.
        receive: Receives messages from WebSocket, saves to Cassandra, and 
                 broadcasts to the room group.
        chat_message: Sends chat messages to the WebSocket.
        get_token_from_query_string: Extracts JWT token from the query string.
        get_user_from_token: Decodes JWT token to retrieve the user object.

    Attributes:
        user: The authenticated user extracted from the JWT token.
        other_user_id: The user ID of the chat partner.
        room_group_name: A unique identifier for the chat room group.

    Example:
        WebSocket URL format: ws://<server>/ws/chat/<other_user_id>/?token=<jwt_token>
        - Connects authenticated users for real-time chatting.
        - Manages sending/receiving of chat messages.
        - Relies on Django Channels for WebSocket communication.
        - Utilizes Cassandra for message persistence.

    Note:
        This consumer is designed to work with a specific frontend implementation 
        that handles the WebSocket protocol and provides a user interface for chat functionality.
    """
    async def connect(self):
        """
        Establishes the WebSocket connection.

        - Extracts and validates the JWT token from the query string.
        - Retrieves the authenticated user based on the token.
        - Sets up the room group name and joins the corresponding group.
        - Accepts the WebSocket connection if authentication succeeds.

        If the token is invalid or absent, closes the connection.
        """
        try:
            self.other_user_id = int(self.scope['url_route']['kwargs']['other_user_id'])
        except ValueError:
            # Handle the error (e.g., close the WebSocket connection or send an error message)
            await self.close(code=4001)  # Custom code indicating invalid input
        
        # Get the token from the query string
        query_string = self.scope['query_string'].decode()
        token = self.get_token_from_query_string(query_string)

        if token:
            # Validate the token and get the user
            user = await self.get_user_from_token(token)
            if user and user.is_authenticated:
                self.user = user
                # Proceed with setting up the WebSocket connection
                
                # Set the room group name based on the connected users
                self.room_group_name = f'chat_{self.user.id}_{self.other_user_id}'

                # Join room group
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                # Accept the WebSocket 
                await self.accept()
                
            else:
                await self.close()
        else:
            await self.close(code=4001)  # Custom code indicating invalid input


    async def disconnect(self, close_code):
        """
        Handles the disconnection of the WebSocket.

        - Leaves the chat room group.
        - Closes the WebSocket connection.

        Parameters:
            close_code (int): The code for the disconnection reason.
        """
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        """
        Receives messages from the WebSocket.

        - Parses the text data as JSON and extracts the message content.
        - Saves the message to the Cassandra database.
        - Broadcasts the message to the room group.

        Parameters:
            text_data (str, optional): The text data received from the WebSocket.
            bytes_data (bytes, optional): The bytes data received from the WebSocket.
        """
        try:
            if text_data:
                text_data_json = json.loads(text_data)
                message = text_data_json['message']
            else:
                message = "testing_else_case_"
            
            # Write message to Cassandra
            save_message(self.user.id, self.other_user_id, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        except json.JSONDecodeError:
            # Handle the error, maybe log it or send an error message back
            print("Received invalid JSON")

    # Receive message from room group
    async def chat_message(self, event):
        """
        Sends messages to the WebSocket.

        - Called by the channel layer when a message is sent to the room group.
        - Sends the chat message over the WebSocket to the client.

        Parameters:
            event (dict): The event containing the message data.
        """
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    def get_token_from_query_string(self, query_string):
        # Extract the token from the query string
        token = ''
        for param in query_string.split('&'):
            if param.startswith('token='):
                token = param.split('=')[1]
                break
        return token

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            # Decode the token
            decoded_token = AccessToken(token)
            
            # Extract user ID and retrieve the user
            user_id = decoded_token["user_id"]  # Access the user ID from the token
            user = User.objects.get(id=user_id)
            return user

        except (InvalidToken, TokenError, User.DoesNotExist):
            # Return AnonymousUser if there's any issue
            return AnonymousUser()
        

#Testing boilerplate
# class EchoConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def receive(self, text_data):
#         await self.send(text_data=text_data)

#class ChatConsumer(AsyncWebsocketConsumer):
    # async def connect(self):
    #     await self.accept()

    # async def disconnect(self, close_code):
    #     pass

    # async def receive(self, text_data=None, bytes_data=None):
    #     pass