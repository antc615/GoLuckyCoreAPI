from django.urls import path
from . import views

urlpatterns = [
    path('matches/', views.match_list, name='match_list'),
    path('swipes/', views.swipe_list_create, name='swipe_list_create'),
    path('favorites/', views.favorites_list_create, name='favorites_list_create'),
]