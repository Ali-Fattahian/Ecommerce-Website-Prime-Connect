from rest_framework import generics, status, permissions
from django.db.models.functions import TruncMonth, TruncDay
from django.db.models import Sum
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


class OrderingFilterExtraPopularOption(OrderingFilter):
    """
    If you pass rating as an ordering param, Add ordering based on
    total number of ratings in addition to the rest of orderings 
    """

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            if 'rating' in ordering:
                return queryset.annotate(
                    total_rating=Sum('review__rating')).order_by('-total_rating', *ordering)[:5]
            return queryset.order_by(*ordering)

        return queryset


class ProductListView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = (
        SearchFilter, OrderingFilterExtraPopularOption, DjangoFilterBackend)
    search_fields = ['name', 'brand', 'subCategory__name',
                     'hasDiscount']  # Add exist(count is stock > 0)
    filterset_fields = ['name', 'brand', 'subCategory__name',
                        'hasDiscount', 'subCategory__category__name']  # Add a price range filter
    ordering_fields = ['name', 'brand', 'subCategory',
                       'price', 'discount', 'createdAt', 'rating']

    # pagination_class = pagination.PageNumberPagination
    # page_size = 15


class PopularProductsListView(generics.ListAPIView):
    queryset = models.Product.objects.annotate(
        total_rating=Sum('review__rating')).order_by('-total_rating')[:4]  # Order by sum of all ratings for the product
    serializer_class = serializers.ProductSerializer


class NewProductsListView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all().order_by('-createdAt')[:4]


class ProductSuggestions(generics.ListAPIView):
    """The goal is to get 5 products from
       the same sub category that have discount"""
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        product = get_object_or_404(models.Product, pk=self.kwargs['pk'])
        products = models.Product.objects.filter(
            subCategory=product.subCategory, hasDiscount=True).exclude(id=product.id).order_by('-createdAt')
        if len(products) > 5:
            products = products[:5]
        return products


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


class CategoryListView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


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
def get_total_annual_orders(request):
    now = datetime.now()
    now_aware = now.replace(tzinfo=pytz.UTC)
    last_year = now_aware - timedelta(days=365)
    last_year_orders = models.Order.objects.filter(
        createdAt__gte=last_year).count()
    return Response(last_year_orders, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_total_monthly_orders(request):
    now = datetime.now()
    now_aware = now.replace(tzinfo=pytz.UTC)
    last_month = now_aware - timedelta(days=30)
    last_month_orders = models.Order.objects.filter(
        createdAt__gte=last_month).count()
    return Response(last_month_orders, status=status.HTTP_200_OK)


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


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_monthly_earnings_by_days(request):
    now = datetime.now()
    now_aware = now.replace(tzinfo=pytz.UTC)
    last_month = now_aware - timedelta(days=30)
    queryset = models.OrderItem.objects.filter(dateCreated__gte=last_month).annotate(day=TruncDay('dateCreated')).values(
        'day')[0:10].annotate(totalEarnings=Sum('price')).values('day', 'totalEarnings')
    monthly_earnings = []
    for obj in queryset:
        monthly_earnings.append({
            'dateCreated': obj['day'],
            'totalEarnings': obj['totalEarnings']
        })
    return Response(monthly_earnings, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_annual_earnings_by_months(request):
    now = datetime.now()
    now_aware = now.replace(tzinfo=pytz.UTC)
    last_year = now_aware - timedelta(days=365)
    queryset = models.OrderItem.objects.filter(dateCreated__gte=last_year).annotate(month=TruncMonth(
        'dateCreated')).values('month').annotate(totalEarnings=Sum('price')).values('month', 'totalEarnings')
    annual_earnings = []
    for obj in queryset:
        annual_earnings.append({
            'dateCreated': obj['month'],
            'totalEarnings': obj['totalEarnings']
        })
    return Response(annual_earnings, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_total_earnings_by_subCategory(request):
    all_order_items = models.OrderItem.objects.all()
    all_sub_categories = models.SubCategory.objects.all()
    earnings = {}

    for obj in all_sub_categories:
        # Make a dictionary in which all sub categories are the keys
        earnings[obj.name] = {'count': 0, 'totalEarnings': 0}

    for obj in all_order_items:
        # In each order item there is only one product
        earnings[obj.product.subCategory.name]['count'] += 1
        earnings[obj.product.subCategory.name]['totalEarnings'] += obj.price
    return Response(earnings, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_total_earnings_by_category(request):
    all_order_items = models.OrderItem.objects.all()
    all_categories = models.Category.objects.all()
    earnings = {}

    for obj in all_categories:
        # Make a dictionary in which all categories are the keys
        earnings[obj.name] = {'count': 0, 'totalEarnings': 0}

    for obj in all_order_items:
        # In each order item there is only one product
        earnings[obj.product.subCategory.category.name]['count'] += 1
        earnings[obj.product.subCategory.category.name]['totalEarnings'] += obj.price
    return Response(earnings, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_total_earnings_by_country(request):
    all_order_items = models.OrderItem.objects.all()
    earnings = {}
    for obj in all_order_items:
        # all_countries_2.append(i)
        if obj.order.shippingaddress.country in earnings.keys():
            earnings[obj.order.shippingaddress.country]['count'] += 1
            earnings[obj.order.shippingaddress.country]['totalEarnings'] += obj.price
        else:
            earnings[obj.order.shippingaddress.country] = {
                'count': 1, 'totalEarnings': obj.price}

    return Response(earnings, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_all_pending_requests(request):
    orders = models.Order.objects.filter(
        isPaid=True, isDelivered=False).count()
    return Response(orders, status=status.HTTP_200_OK)
