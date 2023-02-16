from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, fullname, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')

        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')

        return self.create_user(email, fullname, password, **kwargs)

    def create_user(self, email, fullname, password, **kwargs):
        if not (email and password and fullname):
            raise ValueError(_('The fields must not be empty.'))

        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname, **kwargs)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    fullname = models.CharField(max_length=150)
    join_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    def __str__(self):
        return self.email


# ==================================================================================


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ==================================================================================       


class Product(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, default='', blank=True)
    image1 = models.ImageField(upload_to='products/')
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    brand = models.CharField(max_length=200, default='', blank=True)
    subCategory = models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=355)
    moreDetails = models.TextField(default='', blank=True)
    rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    countInStock = models.IntegerField(
        null=True, blank=True, default=0, validators=[MinValueValidator(0)])
    createdAt = models.DateTimeField(auto_now_add=True)
    hasDiscount = models.BooleanField(default=False)
    discount = models.IntegerField(null=True, blank=True, default=0, validators=[
                                   MinValueValidator(0), MaxValueValidator(99)])

    @property
    def suggests(self):
        products = Product.objects.filter(
            subCategory=self.subCategory, hasDiscount=True)
        if len(products) > 4:
            products = products[:5]
        return products

    def __str__(self):
        return self.name


# ==================================================================================


class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, blank=True, null=True)
    comment = models.TextField(default='', blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)

    
# ==================================================================================


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    paymentMethod = models.CharField(max_length=200, default='', blank=True)
    taxPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.createdAt)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, default='', blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, default='', blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


class ShippingAddress(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, default='', blank=True)
    city = models.CharField(max_length=200, default='', blank=True)
    postalCode = models.CharField(max_length=200, default='', blank=True)
    country = models.CharField(max_length=200, default='', blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.address)