from django.urls import path
from core.views import product_views


urlpatterns = [
    path('', product_views.ProductListView.as_view()),
    path('sub-categories', product_views.SubCategoryListView.as_view()),
    path('create-review/<str:product_id>', product_views.review_create),
    path('brands', product_views.BrandListView.as_view()),
    path('<str:pk>', product_views.ProductDetailView.as_view()),
]
