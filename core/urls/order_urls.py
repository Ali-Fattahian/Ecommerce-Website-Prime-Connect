from django.urls import path
from core.views import order_views

urlpatterns = [
    path('', order_views.OrderListView.as_view()),
    path('get-my-orders', order_views.GetMyOrderView.as_view()),
    path('get-order/<str:pk>', order_views.getOrderView.as_view()),
    path('create', order_views.addOrderItems),
    path('pay/<str:pk>', order_views.update_order_to_paid),
    path('delete-order/<str:pk>', order_views.OrderDeleteView.as_view()),
    path('deliver-order/<str:pk>', order_views.update_order_to_delivered),
]
