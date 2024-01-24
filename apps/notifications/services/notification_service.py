# # apps/notifications/services/notification_service.py

# from ..models import Notification
# from django.contrib.auth import get_user_model

# def handle_like(user_id, content_id):
#     # Example logic for liking content
#     user = get_user_model().objects.get(id=user_id)
    
#     content = Content.objects.get(id=content_id)  # Retrieve the content object based on content_id

#     # Create and save the notification
#     Notification.objects.create(
#         recipient=content.owner,
#         sender=user,
#         notification_type='like',
#         content=f"{user.username} liked your content."
#     )

# def handle_comment(user_id, content_id, comment_text):
#     user = get_user_model().objects.get(id=user_id)
#     content = Content.objects.get(id=content_id)  # Retrieve the content object based on content_id

#     Notification.objects.create(
#         recipient=content.owner,
#         sender=user,
#         notification_type='comment',
#         content=f"{user.username} commented: {comment_text}"
#     )

# def handle_favorite(user_id, content_id):
#     user = get_user_model().objects.get(id=user_id)
#     content = Content.objects.get(id=content_id)  # Retrieve the content object based on content_id

#     Notification.objects.create(
#         recipient=content.owner,
#         sender=user,
#         notification_type='favorite',
#         content=f"{user.username} favorited your content."
#     )
