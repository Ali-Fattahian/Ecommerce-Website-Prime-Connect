from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from core import models
from core import serializers


class ProductListView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['name', 'brand', 'subCategory__name', 'hasDiscount'] # Add exist(count is stock > 0)
    filterset_fields = ['name', 'brand', 'subCategory__name', 'hasDiscount'] # Add a price range filter
    ordering_fields = ['name', 'brand', 'subCategory', 'rating', 'price', 'discount', 'createdAt']
    # pagination_class = pagination.PageNumberPagination
    # page_size = 15


class ProductDetailView(generics.RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


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