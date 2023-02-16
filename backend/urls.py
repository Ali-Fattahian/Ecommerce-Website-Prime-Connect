from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', include('core.urls.product_urls')),
    path('api/orders/', include('core.urls.order_urls')),
    path('api/users/', include('core.urls.user_urls')),
]
