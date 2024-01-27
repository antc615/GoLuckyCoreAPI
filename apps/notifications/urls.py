from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_notifications, name='get_notifications'),
    path('read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('read-all/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
]
