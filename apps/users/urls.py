from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/auth/register', views.register, name='register'),
    path('api/auth/registerLogin/', views.registerLogin, name='registerLogin'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', views.user_profile, name='user_profile'),
    path('api/auth/logout', views.logout, name='logout'),
    path('api/profile/update', views.update_profile, name='update_profile'),
    path('api/profile/delete', views.delete_profile, name='delete_profile'),
    path('api/auth/change-password',  views.change_password, name='change_password'),
    path('api/auth/request-reset-password', views.request_reset_password, name='request_reset_password'),
    path('api/auth/password-reset-confirm', views.password_reset_confirm, name='password_reset_confirm'),
    path('api/profile/deactivate', views.deactivate_account, name='deactivate_account'),
    path('api/profile/reactivate', views.reactivate_account, name='reactivate_account'),
    path('api/profile/preferences', views.user_preferences, name='user_preferences'),
    path('api/profile/upload-image-authenticated', views.upload_image_authenticated, name='upload_image_authenticated'),
    path('api/profile/<int:user_id>/upload-image/', views.upload_image, name='upload-image'),
    path('api/users/<int:user_id>/images/<int:image_id>/delete/', views.delete_image, name='delete-image'),
    path('api/token/refresh/', views.refreshToken, name='refreshToken'),
    path('api/images/<int:image_id>/mark-inactive/', views.mark_image_inactive, name='mark-image-inactive'),
    path('update_images/', views.update_user_images_randomly, name='update_images'),

]