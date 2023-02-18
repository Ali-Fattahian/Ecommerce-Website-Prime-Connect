from django.urls import path
from core.views import product_views


urlpatterns = [
    path('', product_views.ProductListView.as_view()),
    path('<str:pk>', product_views.ProductDetailView.as_view()),
]
