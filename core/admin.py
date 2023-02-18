from django.contrib import admin
from django.contrib.auth import get_user_model
from core import models

admin.site.register(get_user_model()) # Change the name in Admin panel to user (instead of Custom User)
admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(models.SubCategory)
admin.site.register(models.Review)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.ShippingAddress)
