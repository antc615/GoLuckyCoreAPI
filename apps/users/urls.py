from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/auth/register', views.register, name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', views.user_profile, name='user_profile'),
    path('api/auth/logout', views.logout, name='logout'),
    path('api/profile/update', views.update_profile, name='update_profile'),
    path('api/profile/delete', views.delete_profile, name='delete_profile'),
]