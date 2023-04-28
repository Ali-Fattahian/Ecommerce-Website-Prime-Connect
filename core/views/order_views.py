from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from core import serializers, models
import datetime
import pytz


class OrderListView(generics.ListAPIView):
    queryset = models.Order.objects.all().order_by('-id')
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAdminUser]


class GetOrderView(generics.RetrieveAPIView):
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

    try:
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
                                                       price=product.price, image=product.image1.url)
                product.countInStock -= item.qty
                product.save()

        serializer = serializers.OrderSerializer(order, many=False)
        return Response(serializer.data)
    except:
        return Response({'detail': 'All the fields must be provided'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_order_to_paid(request, pk):
    order = get_object_or_404(models.Order, pk=pk)
    if request.user != order.user:
        return Response({'detail': 'You don\'t have the permission to pay for this order'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        totalPrice = request.data['totalPrice']
    except:
        return Response({'detail': 'Total price was\'nt provided'}, status=status.HTTP_400_BAD_REQUEST)

    if totalPrice != str(order.totalPrice):
        return Response({'detail': 'Total price of the order is not correct'}, status=status.HTTP_400_BAD_REQUEST)

    order.isPaid = True

    now_unaware = datetime.datetime.now()
    now_aware = now_unaware.replace(tzinfo=pytz.UTC)
    order.paidAt = now_aware

    order.save()

    return Response({'detail': 'Your payment was successful'}, status=status.HTTP_200_OK)


class OrderDeleteView(generics.DestroyAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAdminUser]


class GetMyOrderView(generics.ListAPIView):
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_list_or_404(models.Order, user=self.request.user)


@api_view(['PUT'])
@permission_classes([permissions.IsAdminUser])
def update_order_to_delivered(request, pk):
    order = get_object_or_404(models.Order, pk=pk)
    order.isDelivered = True

    now_unaware = datetime.datetime.now()
    now_aware = now_unaware.replace(tzinfo=pytz.UTC)
    order.deliveredAt = now_aware

    order.save()

    return Response({'detail': f'Delivered at {order.deliveredAt}'}, status=status.HTTP_200_OK)
