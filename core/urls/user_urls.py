from django.urls import path
from core.views import user_views as views

urlpatterns = [
    path('login', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('register', views.register_user, name='register'),
    path('get-profile/<str:pk>', views.GetUserProfile.as_view(), name='get-profile-pk'),
    path('update-profile/<str:pk>', views.update_user_profile, name='update-profile-pk'),
    path('', views.GetUsers.as_view(), name='get-users'),
]
