from django.urls import path
from core.views import order_views

urlpatterns = [
    path('', order_views.OrderListView.as_view()),
    path('get-order/<str:pk>', order_views.getOrderView.as_view()),
    path('create', order_views.addOrderItems),
]
