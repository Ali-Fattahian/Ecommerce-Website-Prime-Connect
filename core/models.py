from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


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

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


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
        get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='', blank=True)
    image1 = models.ImageField(
        upload_to='products/', default='products/default-image.png', blank=True)
    image2 = models.ImageField(null=True, blank=True, upload_to='products/')
    image3 = models.ImageField(null=True, blank=True, upload_to='products/')
    brand = models.CharField(max_length=200, default='', blank=True)
    subCategory = models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=355)
    moreDetails = models.TextField(default='', blank=True)
    rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    countInStock = models.IntegerField(
        null=True, blank=True, default=0, validators=[MinValueValidator(0)])
    createdAt = models.DateTimeField(auto_now_add=True)
    hasDiscount = models.BooleanField(null=True, blank=True)
    discount = models.IntegerField(blank=True, default=0, validators=[
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
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(default='', blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.rating < 1:
            raise ValidationError(
                _('Rating number equal can not be less than 1.'))
        if self.rating > 5:
            raise ValidationError(
                _('Rating number equal can not be more than 5.'))

    def __str__(self):
        return str(self.rating)


# ==================================================================================


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    paymentMethod = models.CharField(
        max_length=200, default='paypal', blank=True)
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
        return f'{self.user.fullname}\'s order, Price: {self.totalPrice}'


# ==================================================================================


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, default='', blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, default='', blank=True)

    def __str__(self):
        return str(self.name)


# ==================================================================================


class ShippingAddress(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, default='', blank=True)
    city = models.CharField(max_length=200, default='', blank=True)
    postalCode = models.CharField(max_length=200, default='', blank=True)
    country = models.CharField(max_length=200, default='', blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.address)


# ==================================================================================

# class MessageThroughModel(models.Model):
#     message = models.ForeignKey('Message', on_delete=models.CASCADE)
#     AdminMessage = models.ForeignKey('AdminMessage', on_delete=models.CASCADE)


# class Message(models.Model):
#     text = models.TextField(max_length=450)
#     createdAt = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False, blank=True)


# class AdminMessage(models.Model):
#     recipients = models.ManyToManyField(
#         get_user_model(), related_name='recieved_messages')
#     sender = models.ForeignKey(
#         get_user_model(), on_delete=models.CASCADE, related_name='sent_messages')
#     messages = models.ManyToManyField(Message)

#     def __str__(self):
#         return f'Message sent by {self.sender.fullname} on {self.createdAt}'

# class Message(models.Model):
#     user = models.ForeignKey(
#         get_user_model(), on_delete=models.CASCADE, related_name='user')
#     sender = models.ForeignKey(
#         get_user_model(), on_delete=models.CASCADE, related_name='from_user')
#     recipient = models.ForeignKey(
#         get_user_model(), on_delete=models.CASCADE, related_name='to_user')
#     body = models.TextField(max_length=450)
#     date = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     def send_message(from_user, to_user, body):
#         sender_message = Message(
#             user=from_user, sender=from_user, recipient=to_user, body=body, is_read=True)
#         sender_message.save()

#         recipient_message = Message(
#             user=to_user, sender=from_user, recipient=from_user, body=body, is_read=True)
#         recipient_message.save()

#         return sender_message

#     def get_message(user):
#         users = []
#         messages = Message.objects.filter(user=user).values(
#             'recipient').annotate(last=Max('date')).order_by('-last')
#         # filter by user=the login user, recipient=the sender, the lastest message from each sender, order the lastest message by sender using time

#         for message in messages:
#             users.append({
#                 'user': get_user_model().objects.get(pk=message['recipient']),
#                 'last': message['last'],
#                 'unread': Message.objects.filter(user=user, recipient__pk=message['recipient'], is_read=False).count(),
#             })

#         return users


class Message(models.Model):
    content = models.TextField(verbose_name='content')
    recipient = models.ForeignKey(
        get_user_model(), related_name='recipient', on_delete=models.CASCADE)
    sender = models.ForeignKey(
        get_user_model(), related_name='sender', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    isRead = models.BooleanField(default=False)

    def __str__(self):
        return f'From {self.sender} to {self.recipient}'
