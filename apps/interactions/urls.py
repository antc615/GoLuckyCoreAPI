from django.urls import path
from .views import create_like, delete_like, create_comment, create_favorite, delete_favorite

urlpatterns = [
    path('likes/create/<int:image_id>/', create_like, name='create-like'),
    path('likes/delete/<int:like_id>/', delete_like, name='delete-like'),
    path('comments/create/<int:image_id>/', create_comment, name='create-comment'),
    # Add paths for updating and deleting comments
    path('favorites/create/<int:image_id>/', create_favorite, name='create-favorite'),
    path('favorites/delete/<int:favorite_id>/', delete_favorite, name='delete-favorite'),
]