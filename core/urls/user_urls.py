from django.urls import path
from core.views import user_views as views

urlpatterns = [
    path('login', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('register', views.register_user),
    path('profile', views.GetUserProfile.as_view()),
    path('', views.GetUsers.as_view()),
]
