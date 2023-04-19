from django.urls import path
from core.views import user_views as views

urlpatterns = [
    path('login', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('register', views.register_user, name='register'),
    path('get-profile/<str:pk>',
         views.GetUserProfile.as_view(), name='get-profile-pk'),
    path('update-profile/<str:pk>',
         views.update_user_profile, name='update-profile-pk'),
    path('send-message', views.send_message, name='send-message'),
    path('received-messages', views.AllReceivedMessages.as_view(),
         name='received-messages'),
    path('received-messages/change-message-status/<str:pk>',
         views.change_message_status, name='change-message-status'),
    path('received-messages/<str:pk>',
         views.ReceivedMessageDetail.as_view(), name='received-message-detail'),
    path('sent-messages',
         views.AllSentMessages.as_view(), name='sent-messages'),
    path('sent-messages/<str:pk>',
         views.SentMessageDetail.as_view(), name='sent-message-detail'),
    path('admin-list', views.GetAdminUsers.as_view(), name='admin-list'),
    path('', views.GetUsers.as_view(), name='get-users'),
]
