from django.urls import path
from . import views

urlpatterns = [
  path('notifications/', views.add_comment, name='add_comment'),
]
