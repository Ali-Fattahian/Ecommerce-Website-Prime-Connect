from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from decimal import DecimalException
from core.models import (Product, SubCategory,
                         Review, Category,
                         Order, OrderItem,
                         ShippingAddress)


class TestUserCreation(TestCase):
    def setUp(self):
        self.new_user = get_user_model().objects.create_user(
            email='test_user@gmail.com', fullname='Test User', password='a12341234')

        self.new_super_user = get_user_model().objects.create_superuser(
            email='test_super_user@gmail.com', fullname='Test Super User', password='a12341234')

    def test_user_exists(self):
        self.assertIsInstance(self.new_user, get_user_model())

    def test_user_email_normalized(self):
        new_user = get_user_model().objects.create_user(
            email='test_user2@GMAIL.com', fullname='Test User', password='a12341234')
        self.assertEqual(new_user.email, 'test_user2@gmail.com')

    def test_user_fields(self):
        """Fields must be as expected"""
        self.assertEqual(self.new_user.email, 'test_user@gmail.com')
        self.assertEqual(self.new_user.fullname, 'Test User')
        self.assertTrue(self.new_user.check_password('a12341234'))

    def test_user_without_email(self):
        """User instance can't be created without email"""
        with self.assertRaises(TypeError):
            get_user_model().objects.create_user(fullname='Test User', password='a12341234')

    def test_user_without_fullname(self):
        """User instance can't be created without fullname"""
        with self.assertRaises(TypeError):
            get_user_model().objects.create_user(
                email='test_user2@gmail.com', password='a12341234')

    def test_user_non_unique_email(self):
        """User can't be created with an already used email"""
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(email='test_user@gmail.com',
                                                 fullname='Test User', password='a12341234')

    def test_user_without_password(self):
        """User instance can't be created without password"""
        with self.assertRaises(TypeError):
            get_user_model().objects.create_user(
                fullname='Test User', email='test_user2@gmail.com')

    def test_super_user_exists(self):
        self.assertIsInstance(self.new_super_user, get_user_model())

    def test_super_user_fields(self):
        """Fields must be as expected"""
        self.assertEqual(self.new_super_user.email,
                         'test_super_user@gmail.com')
        self.assertEqual(self.new_super_user.fullname, 'Test Super User')
        self.assertTrue(self.new_super_user.check_password('a12341234'))

    def test_super_user_email_normalized(self):
        new_super_user = get_user_model().objects.create_superuser(
            email='test_super_user2@GMAIL.com', fullname='Test Super User', password='a12341234')
        self.assertEqual(new_super_user.email, 'test_super_user2@gmail.com')

    def test_super_user_without_email(self):
        """Super user instance can't be created without email"""
        with self.assertRaises(TypeError):
            get_user_model().objects.create_superuser(
                fullname='Test User', password='a12341234')

    def test_super_user_without_fullname(self):
        """Super user instance can't be created without fullname"""
        with self.assertRaises(TypeError):
            get_user_model().objects.create_superuser(
                email='test_user2@gmail.com', password='a12341234')

    def test_super_user_non_unique_email(self):
        """Super user can't be created with an already used email"""
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_superuser(email='test_super_user@gmail.com',
                                                      fullname='Test Super User', password='a12341234')

    def test_user_without_password(self):
        """Super user instance can't be created without password"""
        with self.assertRaises(TypeError):
            get_user_model().objects.create_superuser(
                fullname='Test Super User', email='test_super_user2@gmail.com')


class TestProduct(TestCase):
    def setUp(self):
        self.new_user = get_user_model().objects.create_user(
            email='test_user@gmail.com', fullname='Test User', password='a12341234')
        self.description = '''new product\'s description,
                            new product\'s description,
                            new product\'s description,
                            new product\'s description.''',

        self.sub_category = SubCategory.objects.create(name="Test Category")
        self.new_product = Product.objects.create(name='new product',
                                                  description=self.description,
                                                  user=self.new_user, brand='Amazon',
                                                  subCategory=self.sub_category, price=499,
                                                  countInStock=12)

    def test_new_product_exists(self):
        self.assertIsInstance(self.new_product, Product)

    def test_new_product_fields(self):
        """Fields must be as expected"""
        self.assertEqual(self.new_product.name, 'new product')
        self.assertEqual(self.new_product.description, self.description)
        self.assertEqual(self.new_product.user, self.new_user)
        self.assertEqual(self.new_product.subCategory, self.sub_category)
        self.assertEqual(self.new_product.price, 499)
        self.assertEqual(self.new_product.countInStock, 12)

    def test_product_without_user(self):
        """Product can be created without a user"""
        with self.assertRaises(IntegrityError):
            Product.objects.create(name='new product',
                                                    description=self.description,
                                                    brand='Amazon',
                                                    subCategory=self.sub_category,
                                                    price=499,
                                                    countInStock=12)

    def test_product_default_image(self):
        """Check if the name of image1 is default-image.png if nothing was provided"""
        self.assertEqual(self.new_product.image1.name.rsplit(
            '/')[-1], 'default-image.png')

    def test_product_other_images(self):
        """image2 and image3 fields should be empty"""
        self.assertEqual(self.new_product.image2, None)
        self.assertEqual(self.new_product.image3, None)


class TestReview(TestCase):
    def setUp(self):
        self.new_user = get_user_model().objects.create_user(
            email='test_user@gmail.com', fullname='Test User', password='a12341234')
        self.sub_category = SubCategory.objects.create(name="Test Category")
        self.new_product = Product.objects.create(name='new product',
                                                  description='''new product\'s description,
                                                  new product\'s description,
                                                  new product\'s description,
                                                  new product\'s description.''',
                                                  user=self.new_user, brand='Amazon',
                                                  subCategory=self.sub_category, price=499,
                                                  countInStock=12)
        self.comment = "This is a test comment"
        self.new_review = Review.objects.create(
            user=self.new_user, product=self.new_product, comment=self.comment, rating=4)

    def test_new_review_exists(self):
        self.assertIsInstance(self.new_review, Review)

    def test_review_fields(self):
        """Fields must be as expected"""
        self.assertEqual(self.new_review.user, self.new_user)
        self.assertEqual(self.new_review.product, self.new_product)
        self.assertEqual(self.new_review.comment, self.comment)
        self.assertEqual(self.new_review.rating, 4)

    def test_review_without_user(self):
        """A review object can not be created without a user"""
        with self.assertRaises(IntegrityError):
            Review.objects.create(
                product=self.new_product, comment=self.comment, rating=4)

    def test_review_without_product(self):
        """A review object can not be created without a product"""
        with self.assertRaises(IntegrityError):
            Review.objects.create(
                user=self.new_user, comment=self.comment, rating=4)

    def test_review_without_rating(self):
        """A review object can not be created without a rating"""
        with self.assertRaises(IntegrityError):
            Review.objects.create(
                user=self.new_user, product=self.new_product, comment=self.comment)

    def test_review_without_comment(self):
        """A review object can be created without a comment"""
        review = Review.objects.create(
            user=self.new_user, product=self.new_product, rating=4)
        self.assertIsInstance(review, Review)


class TestCategory(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name='test category')
        self.assertIsInstance(category, Category)
        self.assertEqual(category.name, 'test category')


class TestSubCategory(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test category')
        self.sub_category = SubCategory.objects.create(
            name='test sub category', category=self.category)

    def test_sub_category_exists(self):
        self.assertIsInstance(self.sub_category, SubCategory)

    def test_sub_category_fields(self):
        """Fields must be as expected"""
        self.assertEqual(self.sub_category.name, 'test sub category')
        self.assertEqual(self.sub_category.category, self.category)


class TestOrder(TestCase):
    def setUp(self):
        self.new_user = get_user_model().objects.create_user(
            email='test_user@gmail.com', fullname='Test User', password='a12341234')
        self.new_order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                              taxPrice=300, totalPrice=3000, shippingPrice=50)

    def test_order_exists(self):
        self.assertIsInstance(self.new_order, Order)

    def test_order_fields(self):
        """Fields must be as expected"""
        self.assertEqual(self.new_order.user, self.new_user)
        self.assertEqual(self.new_order.paymentMethod, 'testmethod')
        self.assertEqual(self.new_order.taxPrice, 300)
        self.assertEqual(self.new_order.totalPrice, 3000)
        self.assertEqual(self.new_order.isDelivered, False)
        self.assertEqual(self.new_order.isPaid, False)

    def test_order_without_user(self):
        """Order can't be created without a user"""
        with self.assertRaises(IntegrityError):
            Order.objects.create(paymentMethod='paypal', shippingPrice=50,
                                 taxPrice=300, totalPrice=3000)

    def test_order_without_method(self):
        """Payment method should be set to paypal if not provided"""
        order = Order.objects.create(user=self.new_user, taxPrice=300,
                                     totalPrice=3000, shippingPrice=50)
        self.assertEqual(order.paymentMethod, 'paypal')

    def test_order_without_shipping_price(self):
        """Order is created without shipping price"""
        order = Order.objects.create(user=self.new_user, taxPrice=300,
                                     totalPrice=3000, paymentMethod='testmethod')

        self.assertIsInstance(order, Order)
        self.assertEqual(order.shippingPrice, None)

    def test_order_without_tax_price(self):
        """Order is created without tax price"""
        order = Order.objects.create(user=self.new_user, shippingPrice=300,
                                     totalPrice=3000, paymentMethod='testmethod')

        self.assertIsInstance(order, Order)
        self.assertEqual(order.taxPrice, None)

    def test_order_without_total_price(self):
        """Order is created without total price"""
        order = Order.objects.create(user=self.new_user, taxPrice=300,
                                     shippingPrice=3000, paymentMethod='testmethod')

        self.assertIsInstance(order, Order)
        self.assertEqual(order.totalPrice, None)


class TestOrderItem(TestCase):
    def setUp(self):
        self.new_user = get_user_model().objects.create_user(
            email='test_user@gmail.com', fullname='Test User', password='a12341234')
        self.description = '''new product\'s description,
                            new product\'s description,
                            new product\'s description,
                            new product\'s description.''',

        self.sub_category = SubCategory.objects.create(name="Test Category")
        self.new_product = Product.objects.create(name='new product',
                                                  description=self.description,
                                                  user=self.new_user, brand='Amazon',
                                                  subCategory=self.sub_category, price=499,
                                                  countInStock=12)
        self.new_order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                              taxPrice=300, totalPrice=3000, shippingPrice=50)
        self.new_order_item = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                       name='testorderitem', qty=4, price=400)

    def test_order_item_exists(self):
        self.assertIsInstance(self.new_order_item, OrderItem)

    def test_order_item_fields(self):
        """Fields must be as expected"""
        self.assertEqual(self.new_order_item.product, self.new_product)
        self.assertEqual(self.new_order_item.order, self.new_order)
        self.assertEqual(self.new_order_item.name, 'testorderitem')
        self.assertEqual(self.new_order_item.qty, 4)
        self.assertEqual(self.new_order_item.price, 400)

    def test_order_item_without_product(self):
        """Order item can be created without product on backend"""
        new_order_item = OrderItem.objects.create(order=self.new_order, name='testorderitem',
                                                  qty=4, price=400)
        self.assertIsInstance(new_order_item, OrderItem)

    def test_order_item_without_order(self):
        """Order item can be created without an order on backend"""
        new_order_item = OrderItem.objects.create(product=self.new_product, name='testorderitem',
                                                  qty=4, price=400)
        self.assertIsInstance(new_order_item, OrderItem)

    def test_order_item_without_name(self):
        """Order item can be created without a name"""
        new_order_item = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                  qty=4, price=400)
        self.assertIsInstance(new_order_item, OrderItem)

    def test_order_item_without_qty(self):
        """Quantity(qty) is 0 if not provided"""
        new_order_item = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                  name='testorderitem', price=400)
        self.assertIsInstance(new_order_item, OrderItem)
        self.assertEqual(new_order_item.qty, 0)

    def test_order_item_without_price(self):
        """Order item can be created without price"""
        new_order_item = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                  name='testorderitem', qty=4)
        self.assertIsInstance(new_order_item, OrderItem)
        self.assertEqual(new_order_item.price, None)

    def test_order_item_price(self):
        """Test the validator of price field(too many digits)"""
        with self.assertRaises(DecimalException):
            OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                     name='testorderitem', qty=4, price=100000)


class TestShippingAddress(TestCase):
    def setUp(self):
        self.new_user = get_user_model().objects.create_user(
            email='test_user@gmail.com', fullname='Test User', password='a12341234')
        self.new_order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                              taxPrice=300, totalPrice=3000, shippingPrice=50)
        self.new_shipping_address = ShippingAddress.objects.create(order=self.new_order, address='testaddress',
                                                                   city='testcity', postalCode=1234,
                                                                   country='testcountry', shippingPrice=100)

    def test_shipping_address_exists(self):
        self.assertIsInstance(self.new_shipping_address, ShippingAddress)

    def test_shipping_address_fields(self):
        """Fields must be as expected"""
        self.assertEqual(self.new_shipping_address.order, self.new_order)
        self.assertEqual(self.new_shipping_address.address, 'testaddress')
        self.assertEqual(self.new_shipping_address.city, 'testcity')
        self.assertEqual(self.new_shipping_address.postalCode, 1234)
        self.assertEqual(self.new_shipping_address.shippingPrice, 100)
        self.assertEqual(self.new_shipping_address.country, 'testcountry')

    def test_shipping_address_with_used_order(self):
        """Same order can not be used for more than 1 shipping address"""
        with self.assertRaises(IntegrityError):
            ShippingAddress.objects.create(address='testaddress', city='testcity',
                                           postalCode=1234, country='testcountry',
                                           shippingPrice=100, order=self.new_order)

    def test_shipping_address_without_order(self):
        """Shipping address can be created without order"""
        shipping_address = ShippingAddress.objects.create(address='testaddress', city='testcity',
                                                          postalCode=1234, country='testcountry',
                                                          shippingPrice=100)
        self.assertIsInstance(shipping_address, ShippingAddress)

    def test_shipping_address_without_address(self):
        """Shipping address can be created without address"""
        order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                     taxPrice=300, totalPrice=3000, shippingPrice=50)
        shipping_address = ShippingAddress.objects.create(order=order, city='testcity',
                                                          postalCode=1234, country='testcountry',
                                                          shippingPrice=100)
        self.assertIsInstance(shipping_address, ShippingAddress)

    def test_shipping_address_without_city(self):
        """Shipping address can be created without city"""
        order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                     taxPrice=300, totalPrice=3000, shippingPrice=50)
        shipping_address = ShippingAddress.objects.create(order=order, address='testaddress',
                                                          postalCode=1234, country='testcountry',
                                                          shippingPrice=100)
        self.assertIsInstance(shipping_address, ShippingAddress)

    def test_shipping_address_without_postal_code(self):
        """Shipping address can be created without postal code"""
        order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                     taxPrice=300, totalPrice=3000, shippingPrice=50)
        shipping_address = ShippingAddress.objects.create(address='testaddress', city='testcity',
                                                          order=order, country='testcountry',
                                                          shippingPrice=100)
        self.assertIsInstance(shipping_address, ShippingAddress)

    def test_shipping_address_without_country(self):
        """Shipping address can be created without country"""
        order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                     taxPrice=300, totalPrice=3000, shippingPrice=50)
        shipping_address = ShippingAddress.objects.create(address='testaddress', city='testcity',
                                                          postalCode=1234, order=order,
                                                          shippingPrice=100)
        self.assertIsInstance(shipping_address, ShippingAddress)

    def test_shipping_address_without_shipping_price(self):
        """Shipping address can be created without shipping price"""
        order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                     taxPrice=300, totalPrice=3000, shippingPrice=50)
        shipping_address = ShippingAddress.objects.create(address='testaddress', city='testcity',
                                                          postalCode=1234, country='testcountry',
                                                          order=order)
        self.assertIsInstance(shipping_address, ShippingAddress)

    def test_order_item_price(self):
        """Test the validator of shipping price field(too many digits)"""
        order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                     taxPrice=300, totalPrice=3000, shippingPrice=50)
        with self.assertRaises(DecimalException):
            ShippingAddress.objects.create(address='testaddress', city='testcity',
                                           postalCode=1234, country='testcountry',
                                           order=order, shippingPrice=100000)
