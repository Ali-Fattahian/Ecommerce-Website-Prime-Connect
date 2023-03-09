from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from core import serializers, models


class OrderListView(generics.ListAPIView):
    queryset = models.Order.objects.all().order_by('-id')
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAdminUser]


class getOrderView(generics.RetrieveAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(models.Order, pk=self.kwargs.get('pk'))
        user = self.request.user
        if user.is_staff or user == obj.user:
            return obj


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        order = models.Order.objects.create(user=user, paymentMethod=data['paymentMethod'],
                                            taxPrice=data['taxPrice'], shippingPrice=data['shippingPrice'],
                                            totalPrice=data['totalPrice'])

        models.ShippingAddress.objects.create(order=order, address=data['shippingAddress']['address'],
                                              city=data['shippingAddress']['city'],
                                              postalCode=data['shippingAddress']['postalCode'],
                                              country=data['shippingAddress']['country'])

        for orderItem in orderItems:
            product = models.Product.objects.get(id=orderItem['id'])
            item = models.OrderItem.objects.create(product=product, order=order,
                                                   name=product.name, qty=orderItem['productQuantity'],
                                                   price=orderItem['price'], image=product.image1.url)
            product.countInStock -= item.qty
            product.save()

    serializer = serializers.OrderSerializer(order, many=False)
    return Response(serializer.data)
