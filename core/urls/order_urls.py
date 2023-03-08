from django.urls import path
from core.views import order_views

urlpatterns = [
    path('', order_views.OrderListView.as_view()),
]
