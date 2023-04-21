from django.urls import path
from core.views import product_views


urlpatterns = [
    path('', product_views.ProductListView.as_view(), name='product-list'),
    path('sub-categories', product_views.SubCategoryListView.as_view(),
         name='sub-category-list'),
    path('create-review/<str:product_id>',
         product_views.review_create, name='create-review'),
    path('create-product', product_views.ProductCreateView.as_view(),
         name='create-product'),
    path('brands', product_views.BrandListView.as_view(), name='brand-list'),
    path('product-edit/<str:pk>',
         product_views.ProductEditView.as_view(), name='product-edit'),
    path('product-image-delete/<str:pk>',
         product_views.delete_product_images, name='product-image-delete'),
    path('get-total-monthly-earnings',
         product_views.get_total_monthly_earnings, name='get-total-monthly-earnings'),
    path('get-total-annual-earnings',
         product_views.get_total_annual_earnings, name='get-total-annual-earnings'),
    path('<str:pk>', product_views.ProductDetailView.as_view(),
         name='product-detail'),
]
