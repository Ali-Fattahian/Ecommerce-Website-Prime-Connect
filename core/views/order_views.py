from rest_framework import generics, permissions
from core import serializers, models


class OrderListView(generics.ListAPIView):
    queryset = models.Order.objects.all().order_by('-id')
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAdminUser]
