from rest_framework import generics, status, permissions
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.core.files import File
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from datetime import datetime, timedelta
import pytz
from core import models
from core import serializers


class ProductListView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['name', 'brand', 'subCategory__name',
                     'hasDiscount']  # Add exist(count is stock > 0)
    filterset_fields = ['name', 'brand', 'subCategory__name',
                        'hasDiscount']  # Add a price range filter
    ordering_fields = ['name', 'brand', 'subCategory',
                       'rating', 'price', 'discount', 'createdAt']
    # pagination_class = pagination.PageNumberPagination
    # page_size = 15


class ProductDetailView(generics.RetrieveDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        if instance.user == self.request.user or self.request.user.is_staff:
            return super().perform_destroy(instance)


class ProductEditView(generics.UpdateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductCreateChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = self.get_object()
        if self.request.user.is_staff == False or self.request.user.id != instance.user.id:
            return Response({'detail': 'You don\'nt have the permission for this request'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().perform_update(serializer)


class ProductCreateView(generics.CreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductCreateChangeSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubCategoryListView(generics.ListAPIView):
    queryset = models.SubCategory.objects.all()
    serializer_class = serializers.SubCategorySerializer


class BrandListView(APIView):
    def get(self, request):
        brands = []
        products = models.Product.objects.all()
        for product in products:
            if product.brand not in brands:
                brands.append(product.brand)
        try:
            serializer = serializers.brand_serializer(brands)
            return Response(serializer, status.HTTP_200_OK)
        except:
            return Response({'error': 'Bad Request'}, status.HTTP_400_BAD_REQUEST)


# class ReviewCreateAPIView(generics.CreateAPIView):
#     queryset = models.Review.objects.all()
#     serializer_class = serializers.ReviewSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'product_id'

#     def perform_create(self, serializer):
#         new_review = self.get_object()
#         prev_review = models.Review.objects.filter(
#             user=new_review.user, product=new_review.product)
#         if prev_review:  # If the user already has a review, replace the new one
#             prev_review.delete()
#         product = get_object_or_404(models.Product, pk=self.kwargs['product_id'])
#         serializer.save(product=product, user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def review_create(request, product_id):
    # Is there a review already
    product = get_object_or_404(models.Product, pk=product_id)
    review_exist = models.Review.objects.filter(
        product=product, user=request.user)
    if review_exist:
        review_exist.delete()
    try:
        review = models.Review.objects.create(product=product, user=request.user,
                                              comment=request.data['comment'], rating=request.data['rating'])
        serializer = serializers.ReviewSerializer(instance=review, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response({"error": "There was a problem submiting your comment, please make sure you have filled all the fields"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def delete_product_images(request, pk):
    """{image1: True, image3: True}, Means set image1, image3 to empty, Don't change image2"""
    product = get_object_or_404(models.Product, pk=pk)
    if request.user.is_staff == False or request.user.id != product.user.id:
        return Response({'detail': 'You don\'nt have the permission for this request'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.data.get('image1'):
        with open(f'{settings.BASE_DIR}/media/products/default-image.png', 'rb') as local_file:
            django_file = File(local_file)
            product.image1.save('default-image.png', django_file)
    if request.data.get('image2'):
        product.image2.delete()
    if request.data.get('image3'):
        product.image3.delete()
    product.save()
    serializer = serializers.ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_total_monthly_earnings(request):
    now = datetime.now()
    now_aware = now.replace(tzinfo=pytz.UTC)
    last_month = now_aware - timedelta(days=30)  # Last 30 days
    last_month_orders = models.OrderItem.objects.filter(
        dateCreated__gte=last_month)
    earnings = 0
    for obj in last_month_orders:
        earnings += obj.price
    return Response(earnings, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_total_annual_earnings(request):
    now = datetime.now()
    now_aware = now.replace(tzinfo=pytz.UTC)
    last_year = now_aware - timedelta(days=365)
    last_year_orders = models.OrderItem.objects.filter(
        dateCreated__gte=last_year)
    earnings = 0
    for obj in last_year_orders:
        earnings += obj.price
    return Response(earnings, status=status.HTTP_200_OK)
