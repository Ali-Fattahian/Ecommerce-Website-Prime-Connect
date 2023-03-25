from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from core import models


class UserSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'fullname', 'isAdmin')

    def get_isAdmin(self, obj):
        return obj.is_staff


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        model = get_user_model()
        fields = ('id', 'token', 'fullname', 'isAdmin', 'email')

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubCategory
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.fullname')

    class Meta:
        model = models.Review
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    # suggests = serializers.ReadOnlyField()
    reviews = serializers.SerializerMethodField(read_only=True)
    numReviews = serializers.SerializerMethodField(read_only=True)
    subCategory = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Product
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

    def get_numReviews(self, obj):
        return obj.review_set.all().count()

    def get_subCategory(self, obj):
        subCategory = obj.subCategory
        serializer = SubCategorySerializer(subCategory)
        return serializer.data
    

class ProductCreateChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShippingAddress
        fields = '__all__'


def brand_serializer(brandList):
    return {
        'brands': brandList
    }


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Order
        fields = ('id', 'orderItems', 'shippingAddress',
                  'user', 'paymentMethod',
                  'taxPrice', 'shippingPrice',
                  'totalPrice', 'isPaid', 'paidAt',
                  'isDelivered', 'deliveredAt',
                  'createdAt')

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(
                obj.shippingaddress, many=False)
            return address.data
        except:
            address = False
            return address

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data
