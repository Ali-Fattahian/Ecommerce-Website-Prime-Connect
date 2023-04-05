from django.urls import path
from core.views import order_views

urlpatterns = [
    path('', order_views.OrderListView.as_view(), name='order-list'),
    path('get-my-orders', order_views.GetMyOrderView.as_view(), name='get-my-order'),
    path('get-order/<str:pk>', order_views.GetOrderView.as_view(), name='get-order'),
    path('create', order_views.addOrderItems, name='create-order-items'),
    path('pay/<str:pk>', order_views.update_order_to_paid, name='pay-order'),
    path('delete-order/<str:pk>',
         order_views.OrderDeleteView.as_view(), name='delete-order'),
    path('deliver-order/<str:pk>',
         order_views.update_order_to_delivered, name='deliver-order'),
]
