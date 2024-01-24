from django.urls import path
from . import views

urlpatterns = [
    path('matches/', views.match_list, name='match_list'),
    path('swipes/', views.swipe_list_create, name='swipe_list_create'),
    path('favorites/', views.favorites_list_create, name='favorites_list_create'),
    path('match-feedback/', views.match_feedback_list_create, name='match_feedback_list_create'),
    path('compatibility-scores/', views.compatibility_score_list_create, name='compatibility_score_list_create'),
    path('match-recommendations/', views.match_recommendation_view, name='match_recommendation_view'),
]