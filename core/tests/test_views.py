from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import (Product, SubCategory,
                         Order, Message,
                         OrderItem, Category,
                         ShippingAddress)
from datetime import datetime, timedelta
import pytz


class TestLoginRoute(APITestCase):
    def setUp(self):
        self.email = 'test_user@gmail.com'
        self.password = 'a12341234'
        self.test_user = get_user_model().objects.create_user(
            email=self.email, password=self.password, fullname='Test User', is_active=True)

    def test_user_exists(self):
        self.assertIsInstance(self.test_user, get_user_model())

    def test_login_route_success(self):
        """Login endpoint should work for an existing user"""
        response = self.client.post(reverse('token_obtain_pair'), data={
                                    'email': self.email, 'password': self.password})
        self.assertEqual(response.status_code, 200)

    def test_login_route_fail_password_field_not_provided(self):
        response = self.client.post(reverse('token_obtain_pair'), data={
                                    'email': self.email})
        self.assertEqual(response.status_code, 400)

    def test_login_route_fail_email_field_not_provided(self):
        response = self.client.post(reverse('token_obtain_pair'), data={
                                    'password': self.password})
        self.assertEqual(response.status_code, 400)

    def test_login_route_fail_wrong_info(self):
        response = self.client.post(reverse('token_obtain_pair'), data={
                                    'email': self.email, 'password': 'a4tadsdgs'})
        self.assertEqual(response.status_code, 401)

    def test_login_route_success_response(self):
        response = self.client.post(reverse('token_obtain_pair'), data={
                                    'email': self.email, 'password': self.password})
        self.assertTrue(b'refresh' in response.content)
        self.assertTrue(b'access' in response.content)
        self.assertTrue(b'token' in response.content)
        self.assertTrue(b'id' in response.content)
        self.assertTrue(b'fullname' in response.content)
        self.assertTrue(b'email' in response.content)
        self.assertTrue(b'isAdmin' in response.content)


class TestRegisterRoute(APITestCase):
    def setUp(self):
        self.fullname = 'Test User'
        self.email = 'test_user@gmail.com'
        self.password = 'a12341234'
        self.response = self.client.post(reverse('register'), data={
            'fullname': self.fullname,
            'email': self.email,
            'password': self.password
        })

    def test_register_route_response_success_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_register_route_response_success_content(self):
        self.assertTrue(b'id' in self.response.content)
        self.assertTrue(b'token' in self.response.content)
        self.assertTrue(b'fullname' in self.response.content)
        self.assertTrue(b'email' in self.response.content)

    def test_user_exists_from_register_route(self):
        self.assertTrue(get_user_model().objects.get(fullname=self.fullname))

    def test_created_user_email_field(self):
        user = get_user_model().objects.get(fullname=self.fullname)
        self.assertEqual(user.email, self.email)

    def test_register_route_fail_wrong_email(self):
        response = self.client.post(reverse('register'), data={
            'fullname': 'test_user_2',
            'email': 'Test Email Wrong',
            'password': self.password
        })
        self.assertEqual(response.status_code, 400)

    def test_register_route_fail_fullname_field_not_provided(self):
        response = self.client.post(reverse('register'), data={
            'email': 'test@gmail.com',
            'password': self.password
        })
        self.assertEqual(response.status_code, 400)

    def test_register_route_fail_email_field_not_provided(self):
        response = self.client.post(reverse('register'), data={
            'fullname': 'test_user_2',
            'password': self.password
        })
        self.assertEqual(response.status_code, 400)

    def test_register_route_fail_password_field_not_provided(self):
        response = self.client.post(reverse('register'), data={
            'fullname': 'test_user_2',
            'email': 'test2@gmail.com',
        })
        self.assertEqual(response.status_code, 400)


class TestGetProfileRoute(APITestCase):
    def setUp(self):
        self.email = 'test_user@gmail.com'
        self.password = 'a12341234'
        self.test_user = get_user_model().objects.create_user(
            email=self.email, password=self.password, fullname='Test User', is_active=True, is_staff=True)
        self.test_user_2 = get_user_model().objects.create_user(
            email='test_user2@gmail.com', password=self.password, fullname='Test User', is_active=True, is_staff=False)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

    def test_get_profile_get_request(self):
        response = self.client.get(
            reverse('get-profile-pk', args=[self.test_user.id]), **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_profile_delete_request_another_user(self):
        response = self.client.delete(
            reverse('get-profile-pk', args=[self.test_user_2.id]), **self.headers)
        self.assertEqual(response.status_code, 204)

    def test_get_profile_delete_request_user(self):
        response = self.client.delete(
            reverse('get-profile-pk', args=[self.test_user.id]), **self.headers)
        self.assertEqual(response.status_code, 204)

    # def test_get_profile_delete_request_not_allowed(self):
    #     """Non staff user can't delete another user"""
    #     login_response = self.client.post(reverse('token_obtain_pair'), data={
    #         'email': 'test_user2@gmail.com', 'password': self.password})

    #     token = login_response.json()['token']
    #     headers = {"HTTP_AUTHORIZATION": f'JWT {token}'}
    #     response = self.client.delete(
    #         reverse('get-profile-pk', args=[self.test_user.id]), **headers)
    #     self.assertEqual(response.status_code, 401)


class TestUpdateUserProfile(APITestCase):
    def setUp(self):
        self.email = 'test_user@gmail.com'
        self.password = 'a12341234'
        self.test_user = get_user_model().objects.create_user(
            email=self.email, password=self.password, fullname='Test User', is_active=True, is_staff=True)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

    def test_update_profile_success_no_password_change(self):
        response = self.client.put(
            reverse('update-profile-pk', args=[self.test_user.id]), data={
                'fullname': 'Test User Changed',
                'email': 'test_user_changed@gmail.com'
            }, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)

        login_new_info_same_password = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user_changed@gmail.com', 'password': self.password
        })

        self.assertEqual(login_new_info_same_password.status_code, 200)

    def test_update_profile_password_success(self):
        """Login should be successful using the changed password"""
        self.new_password = 'newpassword1234'
        response = self.client.put(
            reverse('update-profile-pk', args=[self.test_user.id]), data={
                'password': self.new_password, 'fullname': 'Test User', 'email': self.email
            }, format='json', **self.headers)

        self.assertEqual(response.status_code, 200)

        login_new_info = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.new_password
        })

        self.assertEqual(login_new_info.status_code, 200)

    def test_update_profile_fail_no_fullname(self):
        """Updating profile without prvoding fullname"""
        response = self.client.put(
            reverse('update-profile-pk', args=[self.test_user.id]), data={
                'email': self.email
            }, format='json', **self.headers)

        self.assertEqual(response.status_code, 400)

    def test_update_profile_fail_no_email(self):
        """Updating profile without prvoding email"""
        response = self.client.put(
            reverse('update-profile-pk', args=[self.test_user.id]), data={
                'fullname': 'Test User'
            }, format='json', **self.headers)

        self.assertEqual(response.status_code, 400)


class TestGetUsers(APITestCase):
    def setUp(self):
        self.email = 'test_user@gmail.com'
        self.password = 'a12341234'
        self.test_user = get_user_model().objects.create_user(
            email=self.email, password=self.password, fullname='Test User', is_active=True, is_staff=True)
        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

    def test_get_users_success(self):
        response = self.client.get(
            reverse('get-users'), format='json', **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_users_success_content(self):
        """Only one user exists, So the response should have one user in it"""
        response = self.client.get(
            reverse('get-users'), format='json', **self.headers)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['email'], self.test_user.email)
        self.assertEqual(response.json()[0]
                         ['fullname'], self.test_user.fullname)
        self.assertEqual(response.json()[0]
                         ['isAdmin'], self.test_user.is_staff)

    def test_get_users_fail_no_auth(self):
        """Accessing Get Users route should fail if the user is not authenticated"""
        response = self.client.get(reverse('get-users'))
        self.assertEqual(response.status_code, 401)


class TestProductListView(APITestCase):
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

    def test_product_list_success(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_success_content(self):
        """Only one product exists, So the response should have one product in it"""
        response = self.client.get(reverse('product-list'))
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['brand'], 'Amazon')
        self.assertEqual(response.json()[0]['name'], 'new product')
        self.assertEqual(
            response.json()[0]['subCategory']['name'], self.sub_category.name)
        self.assertEqual(
            response.json()[0]['subCategory']['id'], self.sub_category.id)
        self.assertEqual(response.json()[0]['price'], '499.00')
        self.assertEqual(response.json()[0]['countInStock'], 12)


class TestSubCategoryListView(APITestCase):
    def setUp(self):
        self.name_1 = "Test Category"
        self.name_2 = "Test Category 2"
        SubCategory.objects.create(name=self.name_1)
        SubCategory.objects.create(name=self.name_2)

    def test_sub_category_list_success(self):
        response = self.client.get(reverse('sub-category-list'))
        self.assertEqual(response.status_code, 200)

    def test_sub_category_list_success_content(self):
        """Only two sub categories exist, So the response should have two sub categories in it"""
        response = self.client.get(reverse('sub-category-list'))
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['name'], self.name_1)
        self.assertEqual(response.json()[1]['name'], self.name_2)


class TestCreateReview(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True)
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

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

    def test_create_review_success(self):
        response = self.client.post(reverse('create-review', args=[self.new_product.id]), data={
            'comment': 'new comment',
            'rating': 4
        }, format='json', **self.headers)

        self.assertEqual(response.status_code, 201)

    def test_create_review_success_content(self):
        """Content of the review should be as expected"""
        response = self.client.post(reverse('create-review', args=[self.new_product.id]), data={
            'comment': 'new comment',
            'rating': 4
        }, format='json', **self.headers)
        self.assertEqual(response.json()['user'], self.new_user.fullname)
        self.assertEqual(response.json()['rating'], 4)
        self.assertEqual(response.json()['comment'], 'new comment')
        self.assertEqual(response.json()['product'], self.new_product.id)

    def test_create_review_fail_no_auth(self):
        """Creating a review should fail if the user is not authenticated"""
        response = self.client.post(reverse('create-review', args=[self.new_product.id]), data={
            'comment': 'new comment',
            'rating': 4
        }, format='json')
        self.assertEqual(response.status_code, 401)

    def test_create_review_fail_no_rating(self):
        response = self.client.post(reverse('create-review', args=[self.new_product.id]), data={
            'comment': 'new comment'
        }, format='json', **self.headers)
        self.assertEqual(response.status_code, 400)

    def test_create_review_fail_no_comment(self):
        response = self.client.post(reverse('create-review', args=[self.new_product.id]), data={
            'rating': 4
        }, format='json', **self.headers)
        self.assertEqual(response.status_code, 400)


class TestCreateProduct(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.email_2 = 'test_user2@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)

        self.new_user_2 = get_user_model().objects.create_user(
            email=self.email_2, fullname='Test User 2', password=self.password, is_active=True)

        self.description = 'new product\'s description'

        self.sub_category = SubCategory.objects.create(name="Test Category")

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

    def test_create_product_success(self):
        response = self.client.post(reverse('create-product'), data={
            'name': 'test product',
            'brand': 'test brand',
            'description': self.description,
            'subCategory': self.sub_category.id,
            'rating': 5,
            'price': 399,
            'countInStock': 10,
            'hasDiscount': True,
            'discount': 10,
            'user': self.new_user.id
        }, format='json', **self.headers)

        self.assertEqual(response.status_code, 201)

    def test_create_product_success_content(self):
        """Content of the created product should be as expected"""
        response = self.client.post(reverse('create-product'), data={
            'name': 'test product',
            'brand': 'test brand',
            'description': self.description,
            'subCategory': self.sub_category.id,
            'rating': 5,
            'price': 399,
            'countInStock': 10,
            'hasDiscount': True,
            'discount': 10,
            'user': self.new_user.id
        }, format='json', **self.headers)

        self.assertEqual(response.json()['name'], 'test product')
        self.assertEqual(response.json()['brand'], 'test brand')
        self.assertEqual(response.json()['description'], self.description)
        self.assertEqual(response.json()[
                         'subCategory'], self.sub_category.id)
        self.assertEqual(response.json()['rating'], '5.00')
        self.assertEqual(response.json()['price'], '399.00')
        self.assertEqual(response.json()['countInStock'], 10)
        self.assertEqual(response.json()['hasDiscount'], True)
        self.assertEqual(response.json()['discount'], 10)

    def test_create_product_fail_non_admin(self):
        """A non staff user can't create a product"""
        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email_2, 'password': self.password})

        token = login_response.json()['token']
        headers = {"HTTP_AUTHORIZATION": f'JWT {token}'}

        response = self.client.post(reverse('create-product'), data={
            'name': 'test product',
            'brand': 'test brand',
            'description': self.description,
            'subCategory': self.sub_category.id,
            'rating': 5,
            'price': 399,
            'countInStock': 10,
            'hasDiscount': True,
            'discount': 10,
            'user': self.new_user_2.id
        }, format='json', **headers)
        self.assertEqual(response.status_code, 403)

    def test_create_product_success_no_name(self):
        response = self.client.post(reverse('create-product'), data={
            'brand': 'test brand',
            'description': self.description,
            'subCategory': self.sub_category.id,
            'rating': 5,
            'price': 399,
            'countInStock': 10,
            'hasDiscount': True,
            'discount': 10,
            'user': self.new_user.id
        }, format='json', **self.headers)

        self.assertEqual(response.status_code, 201)

    def test_create_product_success_no_brand(self):
        response = self.client.post(reverse('create-product'), data={
            'name': 'test product',
            'description': self.description,
            'subCategory': self.sub_category.id,
            'rating': 5,
            'price': 399,
            'countInStock': 10,
            'hasDiscount': True,
            'discount': 10,
            'user': self.new_user.id
        }, format='json', **self.headers)

        self.assertEqual(response.status_code, 201)

    def test_create_product_success_no_sub_category(self):
        response = self.client.post(reverse('create-product'), data={
            'name': 'test product',
            'brand': 'test brand',
            'description': self.description,
            'rating': 5,
            'price': 399,
            'countInStock': 10,
            'hasDiscount': True,
            'discount': 10,
            'user': self.new_user.id
        }, format='json', **self.headers)

        self.assertEqual(response.status_code, 201)

    def test_create_product_success_no_rating(self):
        response = self.client.post(reverse('create-product'), data={
            'name': 'test product',
            'brand': 'test brand',
            'description': self.description,
            'subCategory': self.sub_category.id,
            'price': 399,
            'countInStock': 10,
            'hasDiscount': True,
            'discount': 10,
            'user': self.new_user.id
        }, format='json', **self.headers)

        self.assertEqual(response.status_code, 201)

    def test_create_product_success_no_price(self):
        response = self.client.post(reverse('create-product'), data={
            'name': 'test product',
            'brand': 'test brand',
            'description': self.description,
            'subCategory': self.sub_category.id,
            'rating': 5,
            'countInStock': 10,
            'hasDiscount': True,
            'discount': 10,
            'user': self.new_user.id
        }, format='json', **self.headers)

        self.assertEqual(response.status_code, 201)

    def test_create_product_success_no_count_in_stock(self):
        response = self.client.post(reverse('create-product'), data={
            'name': 'test product',
            'brand': 'test brand',
            'description': self.description,
            'subCategory': self.sub_category.id,
            'rating': 5,
            'price': 399,
            'hasDiscount': True,
            'discount': 10,
            'user': self.new_user.id
        }, format='json', **self.headers)

        self.assertEqual(response.status_code, 201)

    def test_create_product_success_no_discount(self):
        response = self.client.post(reverse('create-product'), data={
            'name': 'test product',
            'brand': 'test brand',
            'description': self.description,
            'subCategory': self.sub_category.id,
            'rating': 5,
            'price': 399,
            'countInStock': 10,
            'user': self.new_user.id
        }, format='json', **self.headers)

        self.assertEqual(response.status_code, 201)

    def test_create_product_fail_no_user(self):
        response = self.client.post(reverse('create-product'), data={
            'name': 'test product',
            'brand': 'test brand',
            'description': self.description,
            'subCategory': self.sub_category.id,
            'rating': 5,
            'price': 399,
            'countInStock': 10,
            'hasDiscount': True,
            'discount': 10,
            'user': self.new_user.id
        }, format='json')

        self.assertEqual(response.status_code, 401)

    def test_create_product_fail_no_description(self):
        response = self.client.post(reverse('create-product'), data={
            'name': 'test product',
            'brand': 'test brand',
            'subCategory': self.sub_category.id,
            'rating': 5,
            'price': 399,
            'countInStock': 10,
            'hasDiscount': True,
            'discount': 10,
            'user': self.new_user.id
        }, format='json', **self.headers)

        self.assertEqual(response.status_code, 400)


class TestBrandList(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)
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
        self.new_product_2 = Product.objects.create(name='new product',
                                                    description=self.description,
                                                    user=self.new_user, brand='Apple',
                                                    subCategory=self.sub_category, price=499,
                                                    countInStock=12)

    def test_brand_list_route_success(self):
        response = self.client.get(reverse('brand-list'))
        self.assertEqual(response.status_code, 200)

    def test_brand_list_success_content(self):
        response = self.client.get(reverse('brand-list'))
        self.assertEqual(len(response.json()['brands']), 2)
        self.assertEqual(response.json()['brands'][0], self.new_product.brand)
        self.assertEqual(response.json(
        )['brands'][1], self.new_product_2.brand)


class TestProductEdit(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)
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

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

    def test_update_product_route_success(self):
        response = self.client.put(reverse('product-edit', args=[self.new_product.id]), data={
            'name': 'new product changed',
            'brand': 'brand changed',
            'subCategory': self.sub_category.id,
            'description': 'some new description',
            'rating': 5,
            'price': 399,
            'countInStock': 10,
            'hasDiscount': True,
            'discount': 10,
            'user': self.new_user.id
        }, format='json', **self.headers)

        self.assertEqual(response.status_code, 200)

    def test_update_prodcut_success_content(self):
        response = self.client.put(reverse('product-edit', args=[self.new_product.id]), data={
            'name': 'new product changed',
            'brand': 'brand changed',
            'description': 'some new description',
            'subCategory': None,
            'rating': 5,
            'price': 399,
            'countInStock': 10,
            'hasDiscount': True,
            'discount': 10,
            'user': self.new_user.id
        }, format='json', **self.headers)

        self.assertEqual(response.json()['name'], 'new product changed')
        self.assertEqual(response.json()['brand'], 'brand changed')
        self.assertEqual(response.json()['subCategory'], None)
        self.assertEqual(
            response.json()['description'], 'some new description')
        self.assertEqual(response.json()['rating'], '5.00')
        self.assertEqual(response.json()['price'], '399.00')
        self.assertEqual(response.json()['countInStock'], 10)
        self.assertEqual(response.json()['hasDiscount'], True)
        self.assertEqual(response.json()['discount'], 10)

    def test_update_product_fail_no_user_field(self):
        response = self.client.put(reverse('product-edit', args=[self.new_product.id]), data={
            'name': 'new product changed',
            'brand': 'brand changed',
            'description': 'some new description',
            'subCategory': None,
            'rating': 5,
            'price': 399,
            'countInStock': 10,
            'hasDiscount': True,
            'discount': 10
        }, format='json', **self.headers)

        self.assertEqual(response.status_code, 400)

    def test_update_product_fail_no_user(self):
        response = self.client.put(reverse('product-edit', args=[self.new_product.id]), data={
            'name': 'new product changed',
            'brand': 'brand changed',
            'description': 'some new description',
            'subCategory': None,
            'rating': 5,
            'price': 399,
            'countInStock': 10,
            'hasDiscount': True,
            'discount': 10,
            'user': self.new_user.id
        }, format='json')
        self.assertEqual(response.status_code, 401)

    def test_update_product_success_no_important_fields(self):
        """Updating a product without providing any fields except description and user should be allowed"""
        response = self.client.put(reverse('product-edit', args=[self.new_product.id]), data={
            'description': 'some new description',
            'user': self.new_user.id
        }, format='json', **self.headers)

        self.assertEqual(response.status_code, 200)

    def test_update_product_success_no_field_default(self):
        """Updating a product without providing any fields
           except description and user should'nt change the
           previous values of the product"""
        response = self.client.put(reverse('product-edit', args=[self.new_product.id]), data={
            'description': 'some new description',
            'user': self.new_user.id
        }, format='json', **self.headers)

        self.assertEqual(response.json()['name'], 'new product')
        self.assertEqual(response.json()['brand'], 'Amazon')
        self.assertEqual(response.json()['subCategory'], self.sub_category.id)
        self.assertEqual(response.json()['subCategory'], self.sub_category.id)
        self.assertEqual(response.json()['price'], '499.00')
        self.assertEqual(response.json()['countInStock'], 12)
        self.assertEqual(response.json()['rating'], None)
        self.assertEqual(response.json()['discount'], 0)
        self.assertEqual(response.json()['hasDiscount'], None)
        self.assertEqual(
            response.json()['description'], 'some new description')


class TestProductImageDelete(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)

        self.new_user_2 = get_user_model().objects.create_user(
            email='test_user2@gmail.com', fullname='Test User', password=self.password, is_active=True)

        self.description = '''new product\'s description,
                            new product\'s description,
                            new product\'s description,
                            new product\'s description.''',

        self.sub_category = SubCategory.objects.create(name="Test Category")
        self.new_product = Product.objects.create(name='new product',
                                                  description=self.description,
                                                  user=self.new_user, brand='Amazon',
                                                  subCategory=self.sub_category, price=499,
                                                  countInStock=12, image1='some-name.jpg',
                                                  image2='some-name.jpg',
                                                  image3='some-name.jpg')

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})

        self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user2@gmail.com', 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

    def test_product_images_exist(self):
        self.assertTrue(self.new_product.image1)
        self.assertTrue(self.new_product.image2)
        self.assertTrue(self.new_product.image3)

    def test_delete_images_route_success(self):
        response = self.client.put(reverse('product-image-delete', args=[self.new_product.id]), data={
            'image1': True,
            'image2': True,
            'image3': True
        }, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_images_success_content(self):
        """After deleting image1, image2 and 3,
          Image1 should be set to the default
          image, Image2 and 3 should be set to None"""
        response = self.client.put(reverse('product-image-delete', args=[self.new_product.id]), data={
            'image1': True,
            'image2': True,
            'image3': True
        }, format='json', **self.headers)

        self.assertTrue('default-image' in response.json()['image1'].rsplit(
            '/')[-1])
        self.assertEqual(response.json()['image2'], None)
        self.assertEqual(response.json()['image3'], None)

    def test_delete_image_success_only_image1(self):
        """Deleting only image1 should be allowed"""
        response = self.client.put(reverse('product-image-delete', args=[self.new_product.id]), data={
            'image1': True,
        }, format='json', **self.headers)

        self.assertTrue('default-image' in response.json()['image1'].rsplit(
            '/')[-1])
        self.assertTrue('some-name.jpg' in response.json()['image2'])
        self.assertTrue('some-name.jpg' in response.json()['image3'])

    def test_delete_image_success_only_image2(self):
        """Deleting only image2 should be allowed"""
        response = self.client.put(reverse('product-image-delete', args=[self.new_product.id]), data={
            'image2': True,
        }, format='json', **self.headers)

        self.assertTrue('some-name.jpg' in response.json()['image1'])
        self.assertTrue('some-name.jpg' in response.json()['image3'])
        self.assertEqual(response.json()['image2'], None)

    def test_delete_image_success_only_image3(self):
        """Deleting only image3 should be allowed"""
        response = self.client.put(reverse('product-image-delete', args=[self.new_product.id]), data={
            'image3': True,
        }, format='json', **self.headers)

        self.assertTrue('some-name.jpg' in response.json()['image1'])
        self.assertTrue('some-name.jpg' in response.json()['image2'])
        self.assertEqual(response.json()['image3'], None)

    def test_delete_image_fail_no_auth(self):
        """Non authenticated user can't delete product's pictures"""
        response = self.client.put(reverse('product-image-delete', args=[self.new_product.id]), data={
            'image1': True,
            'image2': True,
            'image3': True
        }, format='json')

        self.assertEqual(response.status_code, 401)

    def test_delete_image_fail_no_staff(self):
        """Only staff members and product creators are allowed to delete images"""
        token = self.login_response_2.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        response = self.client.put(reverse('product-image-delete', args=[self.new_product.id]), data={
            'image1': True,
            'image2': True,
            'image3': True
        }, format='json', **headers)
        self.assertEqual(response.status_code, 401)


class TestProductDetail(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)
        # self.new_user_2 = get_user_model().objects.create_user(
        #     email='test_user2@gmail.com', fullname='Test User', password=self.password, is_active=True)

        self.description = 'new product\'s description'

        self.sub_category = SubCategory.objects.create(name="Test Category")
        self.new_product = Product.objects.create(name='new product',
                                                  description=self.description,
                                                  user=self.new_user, brand='Amazon',
                                                  subCategory=self.sub_category, price=499,
                                                  countInStock=12, image1='some-name.jpg',
                                                  image2='some-name.jpg',
                                                  image3='some-name.jpg')

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        # self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
        #     'email': 'test_user2@gmail.com', 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

    def test_get_product_detail_route_success(self):
        response = self.client.get(
            reverse('product-detail', args=[self.new_product.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_product_detail_success_content(self):
        response = self.client.get(
            reverse('product-detail', args=[self.new_product.id]))

        self.assertEqual(response.json()['name'], self.new_product.name)
        self.assertEqual(
            response.json()['description'], self.new_product.description)
        self.assertEqual(response.json()['brand'], self.new_product.brand)
        self.assertEqual(response.json()['price'],
                         f'{self.new_product.price}.00')
        self.assertEqual(
            response.json()['countInStock'], self.new_product.countInStock)
        self.assertTrue(
            self.new_product.image1.name in response.json()['image1'])
        self.assertTrue(
            self.new_product.image2.name in response.json()['image2'])
        self.assertTrue(
            self.new_product.image3.name in response.json()['image3'])

    def test_delete_product_success(self):
        response = self.client.delete(
            reverse('product-detail', args=[self.new_product.id]), **self.headers)

        self.assertEqual(response.status_code, 204)

    def test_delete_product_fail_no_auth(self):
        response = self.client.delete(
            reverse('product-detail', args=[self.new_product.id]))

        self.assertEqual(response.status_code, 401)

    # def test_delete_product_fail_no_staff(self):
    #     """Only staff members and product creators are allowed to delete the product"""
    #     token = self.login_response_2.json()['token']
    #     headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

    #     response = self.client.delete(
    #         reverse('product-detail', args=[self.new_product.id]), **headers)
    #     self.assertEqual(response.status_code, 403)


class TestOrderList(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)
        self.new_user_2 = get_user_model().objects.create_user(
            email='test_user2@gmail.com', fullname='Test User', password=self.password, is_active=True)
        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user2@gmail.com', 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

        self.new_order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                              taxPrice=300, totalPrice=3000, shippingPrice=50)

    def test_order_list_route_success(self):
        response = self.client.get(reverse('order-list'), **self.headers)

        self.assertEqual(response.status_code, 200)

    def test_order_list_success_content(self):
        response = self.client.get(reverse('order-list'), **self.headers)

        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['paymentMethod'], 'testmethod')
        self.assertEqual(response.json()[0]['taxPrice'], '300.00')
        self.assertEqual(response.json()[0]['totalPrice'], '3000.00')
        self.assertEqual(response.json()[0]['shippingPrice'], '50.00')

    def test_order_list_fail_no_auth(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, 401)

    def test_order_list_fail_no_staff(self):
        token = self.login_response_2.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        response = self.client.get(reverse('order-list'), **headers)
        self.assertEqual(response.status_code, 403)


class TestGetMyOrder(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)
        self.new_user_2 = get_user_model().objects.create_user(
            email='test_user2@gmail.com', fullname='Test User', password=self.password, is_active=True)
        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user2@gmail.com', 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

        self.new_order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                              taxPrice=300, totalPrice=3000, shippingPrice=50)

        self.new_order_2 = Order.objects.create(user=self.new_user, paymentMethod='testmethod2',
                                                taxPrice=400, totalPrice=4000, shippingPrice=60)

    def test_get_my_order_route_success(self):
        response = self.client.get(reverse('get-my-order'), **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_my_order_success_content(self):
        response = self.client.get(reverse('get-my-order'), **self.headers)

        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['paymentMethod'], 'testmethod')
        self.assertEqual(response.json()[0]['taxPrice'], '300.00')
        self.assertEqual(response.json()[0]['totalPrice'], '3000.00')
        self.assertEqual(response.json()[0]['shippingPrice'], '50.00')

        self.assertEqual(response.json()[1]['paymentMethod'], 'testmethod2')
        self.assertEqual(response.json()[1]['taxPrice'], '400.00')
        self.assertEqual(response.json()[1]['totalPrice'], '4000.00')
        self.assertEqual(response.json()[1]['shippingPrice'], '60.00')

    def test_get_my_order_route_fail_no_orders(self):
        """Second user has no orders, So the response should return 404"""
        token = self.login_response_2.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}
        response = self.client.get(reverse('get-my-order'), **headers)

        self.assertEqual(response.status_code, 404)

    def test_get_my_order_fail_no_auth(self):
        response = self.client.get(reverse('get-my-order'))
        self.assertEqual(response.status_code, 401)


class TestGetOrder(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)

        # self.new_user_2 = get_user_model().objects.create_user(
        #     email='test_user2@gmail.com', fullname='Test User', password=self.password, is_active=True)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}
        # self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
        #     'email': 'test_user2@gmail.com', 'password': self.password})

        self.new_order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                              taxPrice=300, totalPrice=3000, shippingPrice=50)

    def test_get_order_route_success(self):
        response = self.client.get(
            reverse('get-order', args=[self.new_order.id]), **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_order_success_content(self):
        response = self.client.get(
            reverse('get-order', args=[self.new_order.id]), **self.headers)
        self.assertEqual(response.json()['paymentMethod'], 'testmethod')
        self.assertEqual(response.json()['taxPrice'], '300.00')
        self.assertEqual(response.json()['totalPrice'], '3000.00')
        self.assertEqual(response.json()['shippingPrice'], '50.00')
        self.assertEqual(response.json()['user']['email'], self.email)
        self.assertEqual(response.json()['user']['fullname'], 'Test User')
        self.assertEqual(response.json()['user']
                         ['isAdmin'], self.new_user.is_staff)

    def test_get_order_fail_no_auth(self):
        response = self.client.get(
            reverse('get-order', args=[self.new_order.id]))
        self.assertEqual(response.status_code, 401)

    # def test_get_order_fail_no_staff(self):
    #     token = self.login_response_2.json()['token']
    #     headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}
    #     response = self.client.get(
    #         reverse('get-order', args=[self.new_order.id]), **headers)

    #     self.assertEqual(response.status_code, 403)


class TestAddOrderItems(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)

        self.sub_category = SubCategory.objects.create(name="Test Category")
        self.new_product = Product.objects.create(name='new product',
                                                  description='Some description',
                                                  user=self.new_user, brand='Amazon',
                                                  subCategory=self.sub_category, price=499,
                                                  countInStock=12, image1='some-name.jpg',
                                                  image2='some-name.jpg',
                                                  image3='some-name.jpg')

        # self.new_user_2 = get_user_model().objects.create_user(
        #     email='test_user2@gmail.com', fullname='Test User', password=self.password, is_active=True)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

    def test_add_order_items_success(self):
        response = self.client.post(
            reverse('create-order-items'), format='json', data={
                'paymentMethod': 'testmethod',
                'shippingPrice': 399,
                'taxPrice': 50,
                'totalPrice': 449,
                'shippingAddress': {
                    'address': 'test address',
                    'city': 'test city',
                    'postalCode': 1234,
                    'country': 'test country'
                },
                'orderItems':
                    [{'id': self.new_product.id, 'productQuantity': 10, 'price': 399}]

            }, **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['orderItems'][0]['name'], self.new_product.name)
        self.assertEqual(response.json()['orderItems'][0]['qty'], 10)
        self.assertEqual(response.json()['orderItems'][0]['price'], '399.00')
        self.assertEqual(
            response.json()['orderItems'][0]['product'], self.new_product.id)
        self.assertTrue(self.new_product.image1.name in response.json()[
                        'orderItems'][0]['image'], self.new_product.id)
        self.assertEqual(
            response.json()['shippingAddress']['address'], 'test address')
        self.assertEqual(
            response.json()['shippingAddress']['city'], 'test city')
        self.assertEqual(
            response.json()['shippingAddress']['postalCode'], '1234')
        self.assertEqual(
            response.json()['shippingAddress']['country'], 'test country')

        self.assertEqual(response.json()['user']['email'], self.new_user.email)
        self.assertEqual(response.json()['user']
                         ['fullname'], self.new_user.fullname)
        self.assertEqual(response.json()['user']
                         ['isAdmin'], self.new_user.is_staff)

        self.assertEqual(response.json()['paymentMethod'], 'testmethod')
        self.assertEqual(response.json()['taxPrice'], '50.00')
        self.assertEqual(response.json()['shippingPrice'], '399.00')
        self.assertEqual(response.json()['totalPrice'], '449.00')

    def test_add_order_items_fail_no_auth(self):
        response = self.client.post(
            reverse('create-order-items'), format='json', data={
                'paymentMethod': 'testmethod',
                'shippingPrice': 399,
                'taxPrice': 50,
                'totalPrice': 449,
                'shippingAddress': {
                    'address': 'test address',
                    'city': 'test city',
                    'postalCode': 1234,
                    'country': 'test country'
                },
                'orderItems':
                    [{'id': self.new_product.id, 'productQuantity': 10, 'price': 399}]

            })
        self.assertEqual(response.status_code, 401)

    def test_add_order_items_fail_no_order_items(self):
        response = self.client.post(
            reverse('create-order-items'), format='json', data={
                'paymentMethod': 'testmethod',
                'shippingPrice': 399,
                'taxPrice': 50,
                'totalPrice': 449,
                'shippingAddress': {
                    'address': 'test address',
                    'city': 'test city',
                    'postalCode': 1234,
                    'country': 'test country'
                },
            }, **self.headers)
        self.assertEqual(response.status_code, 400)

    def test_add_order_items_fail_no_shipping_address(self):
        response = self.client.post(
            reverse('create-order-items'), format='json', data={
                'paymentMethod': 'testmethod',
                'shippingPrice': 399,
                'taxPrice': 50,
                'totalPrice': 449,
                'orderItems':
                    [{'id': self.new_product.id, 'productQuantity': 10, 'price': 399}]

            }, **self.headers)
        self.assertEqual(response.status_code, 400)

    def test_add_order_items_fail_wrong_method(self):
        put_response = self.client.put(
            reverse('create-order-items'), format='json', data={
                'someData': True
            }, **self.headers)
        get_response = self.client.get(
            reverse('create-order-items'), format='json', data={
                'someData': True
            }, **self.headers)

        patch_response = self.client.patch(
            reverse('create-order-items'), format='json', data={
                'someData': True
            }, **self.headers)

        delete_response = self.client.delete(
            reverse('create-order-items'), format='json', data={
                'someData': True
            }, **self.headers)

        self.assertEqual(put_response.status_code, 405)
        self.assertEqual(get_response.status_code, 405)
        self.assertEqual(patch_response.status_code, 405)
        self.assertEqual(delete_response.status_code, 405)


class TestUpdateOrderToPaid(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)

        self.order = Order.objects.create(user=self.new_user, paymentMethod='paymentmethod',
                                          taxPrice=50, shippingPrice=40, totalPrice=400)
        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

    def test_update_order_to_paid_route_success(self):
        response = self.client.put(
            reverse('pay-order', args=[self.order.id]), format='json', data={
                'totalPrice': '400.00'
            }, **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_update_order_to_paid_content_success(self):
        self.assertEqual(self.order.isPaid, False)
        self.client.put(
            reverse('pay-order', args=[self.order.id]), format='json', data={
                'totalPrice': '400.00'
            }, **self.headers)
        self.order.refresh_from_db()
        self.assertEqual(self.order.isPaid, True)

    def test_update_order_to_paid_fail_no_auth(self):
        response = self.client.put(
            reverse('pay-order', args=[self.order.id]), format='json', data={
                'totalPrice': '400.00'
            })
        self.assertEqual(response.status_code, 401)

    def test_update_order_to_paid_fail_no_totalPrice(self):
        response = self.client.put(
            reverse('pay-order', args=[self.order.id]), format='json', **self.headers)
        self.assertEqual(response.status_code, 400)

    def test_update_order_to_paid_fail_wrong_totalPrice(self):
        response = self.client.put(
            reverse('pay-order', args=[self.order.id]), format='json', data={
                'totalPrice': '300.00'
            })
        self.assertEqual(response.status_code, 401)


class TestOrderDelete(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)

        self.order = Order.objects.create(user=self.new_user, paymentMethod='paymentmethod',
                                          taxPrice=50, shippingPrice=40, totalPrice=400)
        self.new_user_2 = get_user_model().objects.create_user(
            email='test_user2@gmail.com', fullname='Test User', password=self.password, is_active=True)
        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user2@gmail.com', 'password': self.password})
        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

    def test_order_delete_success(self):
        response = self.client.delete(
            reverse('delete-order', args=[self.order.id]), **self.headers)

        self.assertEqual(response.status_code, 204)

    def test_order_delete_fail_no_auth(self):
        response = self.client.delete(
            reverse('delete-order', args=[self.order.id]))
        self.assertEqual(response.status_code, 401)

    def test_order_delete_fail_no_staff(self):
        token = self.login_response_2.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}
        response = self.client.delete(
            reverse('delete-order', args=[self.order.id]), **headers)

        self.assertEqual(response.status_code, 403)

    def test_order_delete_fail_wrong_method(self):
        put_response = self.client.put(
            reverse('delete-order', args=[self.order.id]), **self.headers)
        get_response = self.client.get(
            reverse('delete-order', args=[self.order.id]), **self.headers)

        patch_response = self.client.patch(
            reverse('delete-order', args=[self.order.id]), **self.headers)

        post_response = self.client.post(
            reverse('delete-order', args=[self.order.id]), **self.headers)

        self.assertEqual(put_response.status_code, 405)
        self.assertEqual(get_response.status_code, 405)
        self.assertEqual(patch_response.status_code, 405)
        self.assertEqual(post_response.status_code, 405)


class TestUpdateOrderToDelivered(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)

        self.order = Order.objects.create(user=self.new_user, paymentMethod='paymentmethod',
                                          taxPrice=50, shippingPrice=40, totalPrice=400)
        self.new_user_2 = get_user_model().objects.create_user(
            email='test_user2@gmail.com', fullname='Test User', password=self.password, is_active=True)
        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user2@gmail.com', 'password': self.password})
        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

    def test_update_order_to_delivered_route_success(self):
        response = self.client.put(
            reverse('deliver-order', args=[self.order.id]), **self.headers)

        self.assertEqual(response.status_code, 200)

    def test_update_order_to_delivered_content_success(self):
        self.assertFalse(self.order.isDelivered)
        self.client.put(
            reverse('deliver-order', args=[self.order.id]), **self.headers)
        self.order.refresh_from_db()
        self.assertTrue(self.order.isDelivered)

    def test_update_order_to_delivered_fail_no_auth(self):
        response = self.client.put(
            reverse('deliver-order', args=[self.order.id]))

        self.assertEqual(response.status_code, 401)

    def test_update_order_to_delivered_fail_no_staff(self):
        token = self.login_response_2.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        response = self.client.put(
            reverse('deliver-order', args=[self.order.id]), **headers)

        self.assertEqual(response.status_code, 403)

    def test_update_order_to_delivered_fail_wrong_method(self):
        delete_response = self.client.delete(
            reverse('deliver-order', args=[self.order.id]), **self.headers)
        get_response = self.client.get(
            reverse('deliver-order', args=[self.order.id]), **self.headers)

        patch_response = self.client.patch(
            reverse('deliver-order', args=[self.order.id]), **self.headers)

        post_response = self.client.post(
            reverse('deliver-order', args=[self.order.id]), **self.headers)

        self.assertEqual(delete_response.status_code, 405)
        self.assertEqual(get_response.status_code, 405)
        self.assertEqual(patch_response.status_code, 405)
        self.assertEqual(post_response.status_code, 405)


class TestSendMessage(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)

        self.new_user_2 = get_user_model().objects.create_user(
            email='test_user2@gmail.com', fullname='Test User2', password=self.password, is_active=True)

        self.new_user_3 = get_user_model().objects.create_user(
            email='test_user3@gmail.com', fullname='Test User3', password=self.password, is_active=True, is_staff=True)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user2@gmail.com', 'password': self.password})
        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

    def test_send_message_route_success(self):
        response = self.client.post(reverse('send-message'), data={
            'recipient':
                self.new_user_3.id,
            'content': 'test message'
        }, format='json', **self.headers)

        self.assertEqual(response.status_code, 201)

    def test_send_message_success_content(self):
        response = self.client.post(reverse('send-message'), data={
            'recipient':
                self.new_user_3.id,
            'content': 'test message'
        }, format='json', **self.headers)

        self.assertEqual(response.json()['content'], 'test message')
        self.assertEqual(
            response.json()['recipient']['email'], self.new_user_3.email)
        self.assertEqual(
            response.json()['recipient']['fullname'], self.new_user_3.fullname)
        self.assertEqual(
            response.json()['recipient']['isAdmin'], self.new_user_3.is_staff)
        self.assertEqual(
            response.json()['sender']['email'], self.new_user.email)
        self.assertEqual(
            response.json()['sender']['fullname'], self.new_user.fullname)
        self.assertEqual(
            response.json()['sender']['isAdmin'], self.new_user.is_staff)

    def test_send_message_fails_no_auth(self):
        response = self.client.post(reverse('send-message'), data={
            'recipient':
                self.new_user_3.id,
            'content': 'test message'
        }, format='json')

        self.assertEqual(response.status_code, 401)

    def test_send_message_fails_no_staff_sender(self):
        """Only staff members can send messages"""
        token = self.login_response_2.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        response = self.client.post(reverse('send-message'), data={
            'recipient':
                self.new_user_3.id,
            'content': 'test message'
        }, format='json', **headers)

        self.assertEqual(response.status_code, 403)

    def test_send_message_fails_no_staff_recipient(self):
        """Only staff members can receive messages"""
        response = self.client.post(reverse('send-message'), data={
            'recipient':
                self.new_user_2.id,
            'content': 'test message'
        }, format='json', **self.headers)

        self.assertEqual(response.status_code, 400)

    def test_send_message_fails_content_field_not_provided(self):
        response = self.client.post(reverse('send-message'), data={
            'recipient':
                self.new_user_3.id,
        }, format='json', **self.headers)

        self.assertEqual(response.status_code, 400)

    def test_send_message_fails_recipient_field_not_provided(self):
        response = self.client.post(reverse('send-message'), data={
            'content': 'test message'
        }, format='json', **self.headers)

        self.assertEqual(response.status_code, 400)


class TestAllReceivedMessages(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)

        self.new_user_2 = get_user_model().objects.create_user(
            email='test_user2@gmail.com', fullname='Test User2', password=self.password, is_active=True, is_staff=True)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

        self.message_1 = Message.objects.create(sender=self.new_user_2,
                                                recipient=self.new_user, content='test message')
        self.message_2 = Message.objects.create(sender=self.new_user_2,
                                                recipient=self.new_user, content='test message 2')

    def test_all_received_messages_route_success(self):
        response = self.client.get(
            reverse('received-messages'), **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_all_received_messages_success_content(self):
        response = self.client.get(
            reverse('received-messages'), **self.headers)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(
            response.json()[0]['sender']['email'], self.new_user_2.email)
        self.assertEqual(
            response.json()[0]['sender']['fullname'], self.new_user_2.fullname)
        self.assertEqual(
            response.json()[0]['sender']['isAdmin'], self.new_user_2.is_staff)
        self.assertEqual(
            response.json()[0]['recipient']['email'], self.new_user.email)
        self.assertEqual(
            response.json()[0]['recipient']['fullname'], self.new_user.fullname)
        self.assertEqual(
            response.json()[0]['recipient']['isAdmin'], self.new_user.is_staff)
        self.assertEqual(response.json()[0]['content'], 'test message')
        self.assertEqual(response.json()[0]['isRead'], False)
        self.assertEqual(
            response.json()[1]['sender']['email'], self.new_user_2.email)
        self.assertEqual(
            response.json()[1]['sender']['fullname'], self.new_user_2.fullname)
        self.assertEqual(
            response.json()[1]['sender']['isAdmin'], self.new_user_2.is_staff)
        self.assertEqual(
            response.json()[1]['recipient']['email'], self.new_user.email)
        self.assertEqual(
            response.json()[1]['recipient']['fullname'], self.new_user.fullname)
        self.assertEqual(
            response.json()[1]['recipient']['isAdmin'], self.new_user.is_staff)
        self.assertEqual(response.json()[1]['content'], 'test message 2')
        self.assertEqual(response.json()[1]['isRead'], False)

    def test_all_received_messages_fails_no_auth(self):
        response = self.client.get(
            reverse('received-messages'))
        self.assertEqual(response.status_code, 401)

    def test_all_received_messages_fails_wrong_method(self):
        put_response = self.client.put(
            reverse('received-messages'))
        self.assertEqual(put_response.status_code, 401)

        patch_response = self.client.patch(
            reverse('received-messages'))
        self.assertEqual(patch_response.status_code, 401)

        post_response = self.client.post(
            reverse('received-messages'))
        self.assertEqual(post_response.status_code, 401)

        delete_response = self.client.delete(
            reverse('received-messages'))
        self.assertEqual(delete_response.status_code, 401)


class TestAllSentMessages(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)

        self.new_user_2 = get_user_model().objects.create_user(
            email='test_user2@gmail.com', fullname='Test User2', password=self.password, is_active=True, is_staff=True)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

        self.message_1 = Message.objects.create(sender=self.new_user,
                                                recipient=self.new_user_2, content='test message')
        self.message_2 = Message.objects.create(sender=self.new_user,
                                                recipient=self.new_user_2, content='test message 2')

    def test_all_received_messages_route_success(self):
        response = self.client.get(
            reverse('sent-messages'), **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_all_received_messages_success_content(self):
        response = self.client.get(
            reverse('sent-messages'), **self.headers)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(
            response.json()[0]['sender']['email'], self.new_user.email)
        self.assertEqual(
            response.json()[0]['sender']['fullname'], self.new_user.fullname)
        self.assertEqual(
            response.json()[0]['sender']['isAdmin'], self.new_user.is_staff)
        self.assertEqual(
            response.json()[0]['recipient']['email'], self.new_user_2.email)
        self.assertEqual(
            response.json()[0]['recipient']['fullname'], self.new_user_2.fullname)
        self.assertEqual(
            response.json()[0]['recipient']['isAdmin'], self.new_user_2.is_staff)
        self.assertEqual(response.json()[0]['content'], 'test message')
        self.assertEqual(response.json()[0]['isRead'], False)
        self.assertEqual(
            response.json()[1]['sender']['email'], self.new_user.email)
        self.assertEqual(
            response.json()[1]['sender']['fullname'], self.new_user.fullname)
        self.assertEqual(
            response.json()[1]['sender']['isAdmin'], self.new_user.is_staff)
        self.assertEqual(
            response.json()[1]['recipient']['email'], self.new_user_2.email)
        self.assertEqual(
            response.json()[1]['recipient']['fullname'], self.new_user_2.fullname)
        self.assertEqual(
            response.json()[1]['recipient']['isAdmin'], self.new_user_2.is_staff)
        self.assertEqual(response.json()[1]['content'], 'test message 2')
        self.assertEqual(response.json()[1]['isRead'], False)

    def test_all_received_messages_fails_no_auth(self):
        response = self.client.get(
            reverse('sent-messages'))
        self.assertEqual(response.status_code, 401)

    def test_all_received_messages_fails_wrong_method(self):
        put_response = self.client.put(
            reverse('sent-messages'))
        self.assertEqual(put_response.status_code, 401)

        patch_response = self.client.patch(
            reverse('sent-messages'))
        self.assertEqual(patch_response.status_code, 401)

        post_response = self.client.post(
            reverse('sent-messages'))
        self.assertEqual(post_response.status_code, 401)

        delete_response = self.client.delete(
            reverse('sent-messages'))
        self.assertEqual(delete_response.status_code, 401)


class TestReceivedMessageDetail(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)
        self.new_user_2 = get_user_model().objects.create_user(
            email='test_user2@gmail.com', fullname='Test User2', password=self.password, is_active=True, is_staff=True)
        self.new_user_3 = get_user_model().objects.create_user(
            email='test_user3@gmail.com', fullname='Test User3', password=self.password, is_active=True)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user3@gmail.com', 'password': self.password})
        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

        self.message_1 = Message.objects.create(sender=self.new_user,
                                                recipient=self.new_user_2, content='test message')
        self.message_2 = Message.objects.create(sender=self.new_user_2,
                                                recipient=self.new_user, content='test message 2')

    def test_received_message_detail_route_success(self):
        response = self.client.get(
            reverse('received-message-detail', args=[self.message_2.id]), **self.headers)

        self.assertEqual(response.status_code, 200)

    def test_received_message_detail_success_content(self):
        response = self.client.get(
            reverse('received-message-detail', args=[self.message_2.id]), **self.headers)
        self.assertEqual(response.json()['sender']
                         ['email'], self.new_user_2.email)
        self.assertEqual(response.json()['sender']
                         ['fullname'], self.new_user_2.fullname)
        self.assertEqual(response.json()['sender']
                         ['isAdmin'], self.new_user_2.is_staff)
        self.assertEqual(
            response.json()['recipient']['email'], self.new_user.email)
        self.assertEqual(
            response.json()['recipient']['fullname'], self.new_user.fullname)
        self.assertEqual(
            response.json()['recipient']['isAdmin'], self.new_user.is_staff)
        self.assertEqual(response.json()['content'], 'test message 2')
        self.assertEqual(response.json()['isRead'], True)

    def test_received_message_detail_fail_not_recipient(self):
        """Message exists but it should return an empty dictionary because the user is not the recipient of it"""
        response = self.client.get(
            reverse('received-message-detail', args=[self.message_1.id]), **self.headers)
        self.assertEqual(response.json()['content'], '')
        self.assertEqual(response.json()['isRead'], False)
        self.assertEqual(response.json()['sender']['email'], '')
        self.assertEqual(response.json()['sender']['fullname'], '')
        self.assertEqual(response.json()['recipient']['email'], '')
        self.assertEqual(response.json()['recipient']['fullname'], '')

    def test_received_message_detail_fail_no_staff(self):
        token = self.login_response_2.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}
        response = self.client.get(
            reverse('received-message-detail', args=[self.message_1.id]), **headers)
        self.assertEqual(response.status_code, 403)

    def test_received_message_detail_fail_no_auth(self):
        response = self.client.get(
            reverse('received-message-detail', args=[self.message_2.id]))
        self.assertEqual(response.status_code, 401)


class TestSentMessageDetail(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)
        self.new_user_2 = get_user_model().objects.create_user(
            email='test_user2@gmail.com', fullname='Test User2', password=self.password, is_active=True, is_staff=True)
        self.new_user_3 = get_user_model().objects.create_user(
            email='test_user3@gmail.com', fullname='Test User3', password=self.password, is_active=True)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user3@gmail.com', 'password': self.password})
        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

        self.message_1 = Message.objects.create(sender=self.new_user,
                                                recipient=self.new_user_2, content='test message')
        self.message_2 = Message.objects.create(sender=self.new_user_2,
                                                recipient=self.new_user, content='test message 2')

    def test_sent_message_detail_route_success(self):
        response = self.client.get(
            reverse('sent-message-detail', args=[self.message_1.id]), **self.headers)

        self.assertEqual(response.status_code, 200)

    def test_sent_message_detail_success_content(self):
        response = self.client.get(
            reverse('sent-message-detail', args=[self.message_1.id]), **self.headers)
        self.assertEqual(response.json()['sender']
                         ['email'], self.new_user.email)
        self.assertEqual(response.json()['sender']
                         ['fullname'], self.new_user.fullname)
        self.assertEqual(response.json()['sender']
                         ['isAdmin'], self.new_user.is_staff)
        self.assertEqual(
            response.json()['recipient']['email'], self.new_user_2.email)
        self.assertEqual(
            response.json()['recipient']['fullname'], self.new_user_2.fullname)
        self.assertEqual(
            response.json()['recipient']['isAdmin'], self.new_user_2.is_staff)
        self.assertEqual(response.json()['content'], 'test message')
        self.assertEqual(response.json()['isRead'], True)

    def test_sent_message_detail_fail_not_recipient(self):
        """Message exists but it should return an empty dictionary because the user is not the recipient of it"""
        response = self.client.get(
            reverse('sent-message-detail', args=[self.message_2.id]), **self.headers)
        self.assertEqual(response.json()['content'], '')
        self.assertEqual(response.json()['isRead'], False)
        self.assertEqual(response.json()['sender']['email'], '')
        self.assertEqual(response.json()['sender']['fullname'], '')
        self.assertEqual(response.json()['recipient']['email'], '')
        self.assertEqual(response.json()['recipient']['fullname'], '')

    def test_sent_message_detail_fail_no_staff(self):
        token = self.login_response_2.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}
        response = self.client.get(
            reverse('sent-message-detail', args=[self.message_1.id]), **headers)
        self.assertEqual(response.status_code, 403)

    def test_sent_message_detail_fail_no_auth(self):
        response = self.client.get(
            reverse('sent-message-detail', args=[self.message_1.id]))
        self.assertEqual(response.status_code, 401)


class TestChangeMessageStatus(APITestCase):
    def setUp(self):
        self.password = 'a12341234'
        self.email = 'test_user@gmail.com'
        self.new_user = get_user_model().objects.create_user(
            email=self.email, fullname='Test User', password=self.password, is_active=True, is_staff=True)
        self.new_user_2 = get_user_model().objects.create_user(
            email='test_user2@gmail.com', fullname='Test User2', password=self.password, is_active=True, is_staff=True)
        self.new_user_3 = get_user_model().objects.create_user(
            email='test_user3@gmail.com', fullname='Test User3', password=self.password, is_active=True)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user2@gmail.com', 'password': self.password})
        self.login_response_3 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user3@gmail.com', 'password': self.password})
        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

        self.message_1 = Message.objects.create(sender=self.new_user,
                                                recipient=self.new_user_2, content='test message')
        self.message_2 = Message.objects.create(sender=self.new_user_2,
                                                recipient=self.new_user, content='test message 2')

    def test_change_message_status_route_success(self):
        response = self.client.put(reverse('change-message-status', args=[self.message_2.id]), {
            'isRead': True
        }, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_change_message_status_success_content(self):
        response = self.client.put(reverse('change-message-status', args=[self.message_2.id]), {
            'isRead': True
        }, format='json', **self.headers)
        self.assertEqual(response.json()['content'], 'test message 2')
        self.assertEqual(response.json()['sender']
                         ['email'], self.new_user_2.email)
        self.assertEqual(
            response.json()['recipient']['email'], self.new_user.email)
        self.assertEqual(response.json()['isRead'], True)

    def test_change_message_status_fails_no_staff(self):
        """A non staff member can't access this route"""
        token = self.login_response_3.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        response = self.client.put(reverse('change-message-status', args=[self.message_2.id]), {
            'isRead': True
        }, format='json', **headers)

        self.assertEqual(response.status_code, 403)

    def test_change_message_status_fails_no_auth(self):
        response = self.client.put(reverse('change-message-status', args=[self.message_2.id]), {
            'isRead': True
        }, format='json')
        self.assertEqual(response.status_code, 401)

    def test_change_message_status_fails_no_recipient(self):
        """Only the recipient admin is able to access this route"""
        token = self.login_response_2.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}
        response = self.client.put(reverse('change-message-status', args=[self.message_2.id]), {
            'isRead': True
        }, format='json', **headers)
        self.assertEqual(response.status_code, 401)

    def test_change_message_status_fails_no_fields_provided(self):
        response = self.client.put(reverse(
            'change-message-status', args=[self.message_2.id]), format='json', **self.headers)
        self.assertEqual(response.status_code, 400)


class TestGetTotalMonthlyEarnings(APITestCase):
    def setUp(self):
        self.email = 'test_user@gmail.com'
        self.password = 'a12341234'
        self.new_user = get_user_model().objects.create_user(email=self.email,
                                                             fullname='Test User', password=self.password,
                                                             is_active=True, is_staff=True)
        self.new_user_2 = get_user_model().objects.create_user(email='test_user2@gmail.com',
                                                               fullname='Test User', password=self.password,
                                                               is_active=True)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user2@gmail.com', 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

        self.sub_category = SubCategory.objects.create(name="Test Category")
        self.new_product = Product.objects.create(name='new product',
                                                  description='test desciption',
                                                  user=self.new_user, brand='Amazon',
                                                  subCategory=self.sub_category, price=500,
                                                  countInStock=12)
        self.now = datetime.now()
        self.now_aware = self.now.replace(tzinfo=pytz.UTC)
        self.last_month = self.now_aware - timedelta(weeks=5)
        self.new_order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                              taxPrice=300, totalPrice=3000, shippingPrice=50)
        self.new_order_item = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                       name='testorderitem', qty=4, price=2000)
        self.new_order_item_2 = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                         name='testorderitem', qty=2, price=1000)
        self.new_order_item_3 = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                         name='testorderitem', qty=3, price=1500)
        self.new_order_item_3.dateCreated = self.last_month
        self.new_order_item_3.save()  # Was made last month, Shouldn't be in the results

    def test_get_total_monthly_earnings_route_success(self):
        response = self.client.get(
            reverse('get-total-monthly-earnings'), **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_total_monthly_earnings_change_date(self):
        """Set dateCreated for one of the order items to last month and this should change total earnings"""
        self.new_order_item_2.dateCreated = self.last_month
        self.new_order_item_2.save()
        response = self.client.get(
            reverse('get-total-monthly-earnings'), **self.headers)
        self.assertEqual(response.json(), self.new_order_item.price)

    def test_get_total_monthly_earnings_success_content(self):
        response = self.client.get(
            reverse('get-total-monthly-earnings'), **self.headers)
        self.assertEqual(
            response.json(), self.new_order_item.price + self.new_order_item_2.price)

    def test_get_total_monthly_earnings_fails_no_staff(self):
        token = self.login_response_2.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        response = self.client.get(
            reverse('get-total-monthly-earnings'), **headers)
        self.assertEqual(response.status_code, 403)

    def test_get_total_monthly_earnings_fails_no_auth(self):
        response = self.client.get(
            reverse('get-total-monthly-earnings'))
        self.assertEqual(response.status_code, 401)

    def test_get_total_monthly_earnings_fails_wrong_method(self):
        post_response = self.client.post(
            reverse('get-total-monthly-earnings'), **self.headers)
        put_response = self.client.put(
            reverse('get-total-monthly-earnings'), **self.headers)
        patch_response = self.client.patch(
            reverse('get-total-monthly-earnings'), **self.headers)
        delete_response = self.client.delete(
            reverse('get-total-monthly-earnings'), **self.headers)

        self.assertEqual(post_response.status_code, 405)
        self.assertEqual(put_response.status_code, 405)
        self.assertEqual(patch_response.status_code, 405)
        self.assertEqual(delete_response.status_code, 405)


class TestGetTotalAnnualEarnings(APITestCase):
    def setUp(self):
        self.email = 'test_user@gmail.com'
        self.password = 'a12341234'
        self.new_user = get_user_model().objects.create_user(email=self.email,
                                                             fullname='Test User', password=self.password,
                                                             is_active=True, is_staff=True)
        self.new_user_2 = get_user_model().objects.create_user(email='test_user2@gmail.com',
                                                               fullname='Test User', password=self.password,
                                                               is_active=True)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user2@gmail.com', 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

        self.sub_category = SubCategory.objects.create(name="Test Category")
        self.new_product = Product.objects.create(name='new product',
                                                  description='test desciption',
                                                  user=self.new_user, brand='Amazon',
                                                  subCategory=self.sub_category, price=500,
                                                  countInStock=12)
        self.now = datetime.now()
        self.now_aware = self.now.replace(tzinfo=pytz.UTC)
        self.last_year = self.now_aware - timedelta(weeks=60)
        self.new_order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                              taxPrice=300, totalPrice=3000, shippingPrice=50)
        self.new_order_item = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                       name='testorderitem', qty=4, price=2000)
        self.new_order_item_2 = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                         name='testorderitem', qty=2, price=1000)
        self.new_order_item_3 = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                         name='testorderitem', qty=3, price=1500)
        self.new_order_item_3.dateCreated = self.last_year
        self.new_order_item_3.save()  # Was made last year, Shouldn't be in the results

    def test_get_total_annual_earnings_route_success(self):
        response = self.client.get(
            reverse('get-total-annual-earnings'), **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_total_annual_earnings_success_content(self):
        response = self.client.get(
            reverse('get-total-annual-earnings'), **self.headers)
        self.assertEqual(response.json(), 3000)

    def test_get_total_annual_earnings_change_date(self):
        """Set dateCreated for one of the order items to last year and this should change total earnings"""
        self.new_order_item_2.dateCreated = self.last_year
        self.new_order_item_2.save()
        response = self.client.get(
            reverse('get-total-annual-earnings'), **self.headers)
        self.assertEqual(response.json(), self.new_order_item.price)

    def test_get_total_annual_earnings_fails_no_staff(self):
        token = self.login_response_2.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        response = self.client.get(
            reverse('get-total-annual-earnings'), **headers)
        self.assertEqual(response.status_code, 403)

    def test_get_total_annual_earnings_fails_no_auth(self):
        response = self.client.get(
            reverse('get-total-annual-earnings'))
        self.assertEqual(response.status_code, 401)

    def test_get_total_annual_earnings_fails_wrong_method(self):
        post_response = self.client.post(
            reverse('get-total-annual-earnings'), **self.headers)
        put_response = self.client.put(
            reverse('get-total-annual-earnings'), **self.headers)
        patch_response = self.client.patch(
            reverse('get-total-annual-earnings'), **self.headers)
        delete_response = self.client.delete(
            reverse('get-total-annual-earnings'), **self.headers)

        self.assertEqual(post_response.status_code, 405)
        self.assertEqual(put_response.status_code, 405)
        self.assertEqual(patch_response.status_code, 405)
        self.assertEqual(delete_response.status_code, 405)


class TestGetMonthlyEarningsByDays(APITestCase):
    def setUp(self):
        self.email = 'test_user@gmail.com'
        self.password = 'a12341234'
        self.new_user = get_user_model().objects.create_user(email=self.email,
                                                             fullname='Test User', password=self.password,
                                                             is_active=True, is_staff=True)
        self.new_user_2 = get_user_model().objects.create_user(email='test_user2@gmail.com',
                                                               fullname='Test User', password=self.password,
                                                               is_active=True)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user2@gmail.com', 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

        self.sub_category = SubCategory.objects.create(name="Test Category")
        self.new_product = Product.objects.create(name='new product',
                                                  description='test desciption',
                                                  user=self.new_user, brand='Amazon',
                                                  subCategory=self.sub_category, price=500,
                                                  countInStock=12)
        self.now = datetime.now()
        self.now_aware = self.now.replace(tzinfo=pytz.UTC)
        self.last_month = self.now_aware - timedelta(weeks=5)
        self.new_order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                              taxPrice=300, totalPrice=3000, shippingPrice=50)
        self.new_order_item = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                       name='testorderitem', qty=4, price=2000)
        self.new_order_item_2 = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                         name='testorderitem', qty=2, price=1000)
        self.new_order_item_3 = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                         name='testorderitem', qty=3, price=1500)
        yesterday = self.now_aware - timedelta(days=1)
        self.new_order_item_2.dateCreated = yesterday
        self.new_order_item_2.save()

        self.new_order_item_3.dateCreated = self.last_month
        self.new_order_item_3.save()  # Was made last month, Shouldn't be in the results

    def test_get_monthly_earnings_by_days_route_success(self):
        response = self.client.get(
            reverse('get-monthly-earnings-by-days'), **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_monthly_earnings_by_days_route_success(self):
        response = self.client.get(
            reverse('get-monthly-earnings-by-days'), **self.headers)
        # Two orders are in this month, Separate days
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[1]['dateCreated'][0:10], str(
            self.new_order_item.dateCreated)[0:10])
        self.assertEqual(response.json()[0]['dateCreated'][0:10], str(
            self.new_order_item_2.dateCreated)[0:10])
        self.assertEqual(
            response.json()[1]['totalEarnings'], self.new_order_item.price)
        self.assertEqual(
            response.json()[0]['totalEarnings'], self.new_order_item_2.price)

    def test_get_monthly_earnings_by_days_change_date(self):
        """Set dateCreated for one of the order items to last month and this should change th earnings result"""
        self.new_order_item_2.dateCreated = self.last_month
        self.new_order_item_2.save()

        response = self.client.get(
            reverse('get-monthly-earnings-by-days'), **self.headers)
        self.assertEqual(len(response.json()), 1)

    def test_get_monthly_earnings_by_days_fails_no_staff(self):
        token = self.login_response_2.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        response = self.client.get(
            reverse('get-monthly-earnings-by-days'), **headers)
        self.assertEqual(response.status_code, 403)

    def test_get_monthly_earnings_by_days_fails_no_auth(self):
        response = self.client.get(
            reverse('get-monthly-earnings-by-days'))
        self.assertEqual(response.status_code, 401)

    def test_get_monthly_earnings_by_days_fails_wrong_method(self):
        post_response = self.client.post(
            reverse('get-monthly-earnings-by-days'), **self.headers)
        self.assertEqual(post_response.status_code, 405)

        put_response = self.client.put(
            reverse('get-monthly-earnings-by-days'), **self.headers)
        self.assertEqual(put_response.status_code, 405)

        patch_response = self.client.patch(
            reverse('get-monthly-earnings-by-days'), **self.headers)
        self.assertEqual(patch_response.status_code, 405)

        delete_response = self.client.delete(
            reverse('get-monthly-earnings-by-days'), **self.headers)
        self.assertEqual(delete_response.status_code, 405)


class TestGetAnnualEarningsByMonths(APITestCase):
    def setUp(self):
        self.email = 'test_user@gmail.com'
        self.password = 'a12341234'
        self.new_user = get_user_model().objects.create_user(email=self.email,
                                                             fullname='Test User', password=self.password,
                                                             is_active=True, is_staff=True)
        self.new_user_2 = get_user_model().objects.create_user(email='test_user2@gmail.com',
                                                               fullname='Test User', password=self.password,
                                                               is_active=True)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user2@gmail.com', 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

        self.sub_category = SubCategory.objects.create(name="Test Category")
        self.new_product = Product.objects.create(name='new product',
                                                  description='test desciption',
                                                  user=self.new_user, brand='Amazon',
                                                  subCategory=self.sub_category, price=500,
                                                  countInStock=12)
        self.now = datetime.now()
        self.now_aware = self.now.replace(tzinfo=pytz.UTC)
        self.last_year = self.now_aware - timedelta(weeks=60)
        self.last_month = self.now_aware - timedelta(weeks=5)
        self.new_order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                              taxPrice=300, totalPrice=3000, shippingPrice=50)
        self.new_order_item = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                       name='testorderitem', qty=4, price=2000)
        self.new_order_item_2 = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                         name='testorderitem', qty=2, price=1000)
        self.new_order_item_3 = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                         name='testorderitem', qty=3, price=1500)
        self.new_order_item_2.dateCreated = self.last_month
        self.new_order_item_2.save()  # Different month to make them separated
        self.new_order_item_3.dateCreated = self.last_year
        self.new_order_item_3.save()  # Was made last year, Shouldn't be in the results

    def test_get_annual_earnings_by_months_route_success(self):
        response = self.client.get(
            reverse('get-annual-earnings-by-months'), **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_annual_earnings_by_months_success_content(self):
        response = self.client.get(
            reverse('get-annual-earnings-by-months'), **self.headers)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[1]['dateCreated'][0:7], str(
            self.new_order_item.dateCreated)[0:7])
        self.assertEqual(response.json()[0]['dateCreated'][0:7], str(
            self.new_order_item_2.dateCreated)[0:7])
        self.assertEqual(
            response.json()[1]['totalEarnings'], self.new_order_item.price)
        self.assertEqual(
            response.json()[0]['totalEarnings'], self.new_order_item_2.price)

    def test_get_annual_earnings_by_months_change_date_to_this_month(self):
        """Set dateCreated for order item 2 to this month should add the price of that to earnings of this month"""
        self.new_order_item_2.dateCreated = self.now_aware
        self.new_order_item_2.save()
        response = self.client.get(
            reverse('get-annual-earnings-by-months'), **self.headers)

        self.assertEqual(len(response.json()), 1)
        self.assertEqual(
            response.json()[0]['totalEarnings'],
            self.new_order_item.price + self.new_order_item_2.price)  # Now they are in the same month
        self.assertEqual(
            response.json()[0]['dateCreated'][0:7],
            str(self.new_order_item.dateCreated)[0:7])  # From the beginning to the month is important

    def test_get_annual_earnings_by_months_change_date_to_this_year(self):
        """Settings order item 3 dateCreated to this year and separate month should add it to the results"""
        self.new_order_item_3.dateCreated = self.now_aware - \
            timedelta(weeks=11)
        self.new_order_item_3.save()
        response = self.client.get(
            reverse('get-annual-earnings-by-months'), **self.headers)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(
            response.json()[0]['totalEarnings'], self.new_order_item_3.price)
        self.assertEqual(response.json()[0]['dateCreated'][0:7], str(
            self.new_order_item_3.dateCreated)[0:7])

    def test_get_annual_earnings_by_months_fails_no_staff(self):
        token = self.login_response_2.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}
        response = self.client.get(
            reverse('get-annual-earnings-by-months'), **headers)

        self.assertEqual(response.status_code, 403)

    def test_get_annual_earnings_by_months_fails_no_auth(self):
        response = self.client.get(reverse('get-annual-earnings-by-months'))

        self.assertEqual(response.status_code, 401)

    def test_get_annual_earnings_by_months_fails_wrong_method(self):
        post_response = self.client.post(
            reverse('get-annual-earnings-by-months'), **self.headers)
        self.assertEqual(post_response.status_code, 405)

        put_response = self.client.put(
            reverse('get-annual-earnings-by-months'), **self.headers)
        self.assertEqual(put_response.status_code, 405)

        patch_response = self.client.patch(
            reverse('get-annual-earnings-by-months'), **self.headers)
        self.assertEqual(patch_response.status_code, 405)

        delete_response = self.client.delete(
            reverse('get-annual-earnings-by-months'), **self.headers)
        self.assertEqual(delete_response.status_code, 405)


class TestGetTotalEarningsBySubCategory(APITestCase):
    def setUp(self):
        self.email = 'test_user@gmail.com'
        self.password = 'a12341234'
        self.new_user = get_user_model().objects.create_user(email=self.email,
                                                             fullname='Test User', password=self.password,
                                                             is_active=True, is_staff=True)
        self.new_user_2 = get_user_model().objects.create_user(email='test_user2@gmail.com',
                                                               fullname='Test User', password=self.password,
                                                               is_active=True)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user2@gmail.com', 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

        self.sub_category = SubCategory.objects.create(name="Test Category")
        self.sub_category_2 = SubCategory.objects.create(
            name="Test Category 2")
        self.sub_category_3 = SubCategory.objects.create(
            name="Test Category 3")

        self.new_product = Product.objects.create(name='new product',
                                                  description='test desciption',
                                                  user=self.new_user, brand='Amazon',
                                                  subCategory=self.sub_category, price=500,
                                                  countInStock=12)
        self.new_product_2 = Product.objects.create(name='new product 2',
                                                    description='test desciption 2',
                                                    user=self.new_user, brand='Apple',
                                                    subCategory=self.sub_category_2, price=500,
                                                    countInStock=12)
        self.new_product_3 = Product.objects.create(name='new product 3',
                                                    description='test desciption 3',
                                                    user=self.new_user, brand='Sony',
                                                    subCategory=self.sub_category_3, price=500,
                                                    countInStock=12)

        self.new_order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                              taxPrice=300, totalPrice=3000, shippingPrice=50)
        self.new_order_item = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                       name='testorderitem', qty=4, price=2000)
        self.new_order_item_2 = OrderItem.objects.create(product=self.new_product_2, order=self.new_order,
                                                         name='testorderitem', qty=2, price=1000)
        self.new_order_item_3 = OrderItem.objects.create(product=self.new_product_3, order=self.new_order,
                                                         name='testorderitem', qty=3, price=1500)

    def test_get_total_earnings_by_sub_category_route_success(self):
        response = self.client.get(
            reverse('get-total-earnings-by-subCategory'), **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_total_earnings_by_sub_category_success_content(self):
        response = self.client.get(
            reverse('get-total-earnings-by-subCategory'), **self.headers)

        self.assertEqual(len(response.json()), 3)

        self.assertTrue(response.json()[self.sub_category.name])
        self.assertTrue(response.json()[self.sub_category_2.name])
        self.assertTrue(response.json()[self.sub_category_3.name])

        self.assertEqual(response.json()[
                         self.sub_category.name]['totalEarnings'],
                         self.new_order_item.price)
        self.assertEqual(response.json()[
                         self.sub_category_2.name]['totalEarnings'],
                         self.new_order_item_2.price)
        self.assertEqual(response.json()[
                         self.sub_category_3.name]['totalEarnings'],
                         self.new_order_item_3.price)

    def test_get_total_earnings_by_sub_category_change_sub_categories(self):
        """By setting all sub categories to one, We should still
          get three dictionories in the results,
          And all the dictionaries should have different numbers"""
        self.new_product_2.subCategory = self.sub_category
        self.new_product_2.save()
        self.new_product_3.subCategory = self.sub_category
        self.new_product_3.save()

        response = self.client.get(
            reverse('get-total-earnings-by-subCategory'), **self.headers)

        self.assertEqual(len(response.json()), 3)
        self.assertTrue(response.json()[self.sub_category.name])
        self.assertTrue(response.json()[self.sub_category_2.name])
        self.assertTrue(response.json()[self.sub_category_3.name])

        self.assertEqual(response.json()[self.sub_category.name]['totalEarnings'],
                         self.new_order_item.price + self.new_order_item_2.price
                         + self.new_order_item_3.price)
        self.assertEqual(
            response.json()[self.sub_category_2.name]['totalEarnings'], 0)
        self.assertEqual(
            response.json()[self.sub_category_3.name]['totalEarnings'], 0)
        self.assertEqual(response.json()[self.sub_category.name]['count'], 3)
        self.assertEqual(response.json()[self.sub_category_2.name]['count'], 0)
        self.assertEqual(response.json()[self.sub_category_3.name]['count'], 0)

    def test_get_total_earnings_by_sub_category_fails_no_staff(self):
        token = self.login_response_2.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        response = self.client.get(
            reverse('get-total-earnings-by-subCategory'), **headers)

        self.assertEqual(response.status_code, 403)

    def test_get_total_earnings_by_sub_category_fails_no_auth(self):
        response = self.client.get(
            reverse('get-total-earnings-by-subCategory'))

        self.assertEqual(response.status_code, 401)

    def test_get_total_earnings_by_sub_category_fails_wrong_method(self):
        post_response = self.client.post(
            reverse('get-total-earnings-by-subCategory'), **self.headers)
        self.assertEqual(post_response.status_code, 405)

        put_response = self.client.put(
            reverse('get-total-earnings-by-subCategory'), **self.headers)
        self.assertEqual(put_response.status_code, 405)

        patch_response = self.client.patch(
            reverse('get-total-earnings-by-subCategory'), **self.headers)
        self.assertEqual(patch_response.status_code, 405)

        delete_response = self.client.delete(
            reverse('get-total-earnings-by-subCategory'), **self.headers)
        self.assertEqual(delete_response.status_code, 405)


class TestGetTotalEarningsByCategory(APITestCase):
    def setUp(self):
        self.email = 'test_user@gmail.com'
        self.password = 'a12341234'
        self.new_user = get_user_model().objects.create_user(email=self.email,
                                                             fullname='Test User', password=self.password,
                                                             is_active=True, is_staff=True)
        self.new_user_2 = get_user_model().objects.create_user(email='test_user2@gmail.com',
                                                               fullname='Test User', password=self.password,
                                                               is_active=True)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user2@gmail.com', 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

        self.category_1 = Category.objects.create(name='Test Category')
        self.category_2 = Category.objects.create(name='Test Category 2')
        self.sub_category = SubCategory.objects.create(
            name="Test Sub Category", category=self.category_1)
        self.sub_category_2 = SubCategory.objects.create(
            name="Test Sub Category 2", category=self.category_1)

        self.sub_category_3 = SubCategory.objects.create(
            name="Test Sub Category 3", category=self.category_2)

        self.new_product = Product.objects.create(name='new product',
                                                  description='test desciption',
                                                  user=self.new_user, brand='Amazon',
                                                  subCategory=self.sub_category, price=500,
                                                  countInStock=12)
        self.new_product_2 = Product.objects.create(name='new product 2',
                                                    description='test desciption 2',
                                                    user=self.new_user, brand='Apple',
                                                    subCategory=self.sub_category_2, price=500,
                                                    countInStock=12)
        self.new_product_3 = Product.objects.create(name='new product 3',
                                                    description='test desciption 3',
                                                    user=self.new_user, brand='Sony',
                                                    subCategory=self.sub_category_3, price=500,
                                                    countInStock=12)
        self.new_order = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                              taxPrice=300, totalPrice=3000, shippingPrice=50)
        self.new_order_item = OrderItem.objects.create(product=self.new_product, order=self.new_order,
                                                       name='testorderitem', qty=4, price=2000)
        self.new_order_item_2 = OrderItem.objects.create(product=self.new_product_2, order=self.new_order,
                                                         name='testorderitem', qty=2, price=1000)
        self.new_order_item_3 = OrderItem.objects.create(product=self.new_product_3, order=self.new_order,
                                                         name='testorderitem', qty=3, price=1500)

    def test_get_total_earnings_by_category_route_success(self):
        response = self.client.get(
            reverse('get-total-earnings-by-category'), **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_total_earnings_by_category_success_content(self):
        response = self.client.get(
            reverse('get-total-earnings-by-category'), **self.headers)

        self.assertEqual(len(response.json()), 2)

        self.assertTrue(response.json()[self.category_1.name])
        self.assertTrue(response.json()[self.category_2.name])

        self.assertEqual(response.json()[
                         self.category_1.name]['totalEarnings'],
                         self.new_order_item.price + self.new_order_item_2.price)
        self.assertEqual(response.json()[
                         self.category_1.name]['count'], 2)

        self.assertEqual(response.json()[
                         self.category_2.name]['count'], 1)

    def test_get_total_earnings_by_category_change_sub_category(self):
        """Changing the category of the 3rd sub category should result in different numbers"""
        self.sub_category_3.category = self.category_1
        self.sub_category_3.save()

        response = self.client.get(
            reverse('get-total-earnings-by-category'), **self.headers)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[self.category_1.name]['totalEarnings'], self.new_order_item.price +
                         self.new_order_item_2.price + self.new_order_item_3.price)
        self.assertEqual(response.json()[self.category_1.name]['count'], 3)
        self.assertEqual(
            response.json()[self.category_2.name]['totalEarnings'], 0)
        self.assertEqual(response.json()[self.category_2.name]['count'], 0)

    def test_get_total_earnings_by_category_fails_no_staff(self):
        token = self.login_response_2.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        response = self.client.get(
            reverse('get-total-earnings-by-category'), **headers)
        self.assertEqual(response.status_code, 403)

    def test_get_total_earnings_by_category_fails_no_auth(self):
        response = self.client.get(
            reverse('get-total-earnings-by-category'))
        self.assertEqual(response.status_code, 401)

    def test_get_total_earnings_by_category_fails_wrong_method(self):
        post_response = self.client.post(
            reverse('get-total-earnings-by-category'), **self.headers)
        self.assertEqual(post_response.status_code, 405)

        put_response = self.client.put(
            reverse('get-total-earnings-by-category'), **self.headers)
        self.assertEqual(put_response.status_code, 405)

        patch_response = self.client.patch(
            reverse('get-total-earnings-by-category'), **self.headers)
        self.assertEqual(patch_response.status_code, 405)

        delete_response = self.client.delete(
            reverse('get-total-earnings-by-category'), **self.headers)
        self.assertEqual(delete_response.status_code, 405)


class TestGetTotalEarningsByCountry(APITestCase):
    def setUp(self):
        self.email = 'test_user@gmail.com'
        self.password = 'a12341234'
        self.new_user = get_user_model().objects.create_user(email=self.email,
                                                             fullname='Test User', password=self.password,
                                                             is_active=True, is_staff=True)
        self.new_user_2 = get_user_model().objects.create_user(email='test_user2@gmail.com',
                                                               fullname='Test User', password=self.password,
                                                               is_active=True)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user2@gmail.com', 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

        self.sub_category = SubCategory.objects.create(
            name="Test Sub Category")
        self.new_product = Product.objects.create(name='new product',
                                                  description='test desciption',
                                                  user=self.new_user, brand='Amazon',
                                                  subCategory=self.sub_category, price=500,
                                                  countInStock=12)
        self.new_product_2 = Product.objects.create(name='new product 2',
                                                    description='test desciption 2',
                                                    user=self.new_user, brand='Apple',
                                                    subCategory=self.sub_category, price=500,
                                                    countInStock=12)
        self.new_product_3 = Product.objects.create(name='new product 3',
                                                    description='test desciption 3',
                                                    user=self.new_user, brand='Sony',
                                                    subCategory=self.sub_category, price=500,
                                                    countInStock=12)

        self.new_order_1 = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                                taxPrice=300, totalPrice=3350, shippingPrice=50)
        self.new_order_item = OrderItem.objects.create(product=self.new_product, order=self.new_order_1,
                                                       name='testorderitem', qty=4, price=2000)
        self.new_order_item_2 = OrderItem.objects.create(product=self.new_product_2, order=self.new_order_1,
                                                         name='testorderitem', qty=2, price=1000)
        self.new_shipping_address_1 = ShippingAddress.objects.create(order=self.new_order_1, address='testaddress',
                                                                     city='Test City 1', postalCode=1234,
                                                                     country='Test Country 1')

        self.new_order_2 = Order.objects.create(user=self.new_user, paymentMethod='testmethod',
                                                taxPrice=50, totalPrice=1600, shippingPrice=50)
        self.new_order_item_3 = OrderItem.objects.create(product=self.new_product_3, order=self.new_order_2,
                                                         name='testorderitem', qty=3, price=1500)

        self.new_shipping_address_2 = ShippingAddress.objects.create(order=self.new_order_2, address='testaddress',
                                                                     city='Test City 2', postalCode=1234,
                                                                     country='Test Country 2')

    def test_get_total_earnings_by_country_route_success(self):
        response = self.client.get(
            reverse('get-total-earnings-by-country'), **self.headers)

        self.assertEqual(response.status_code, 200)

    def test_get_total_earnings_by_country_success_content(self):
        response = self.client.get(
            reverse('get-total-earnings-by-country'), **self.headers)
        self.assertEqual(len(response.json()), 2)
        self.assertTrue(response.json()[self.new_shipping_address_1.country])
        self.assertTrue(response.json()[self.new_shipping_address_2.country])
        self.assertEqual(response.json()[self.new_shipping_address_1.country]['totalEarnings'],
                         self.new_order_item.price + self.new_order_item_2.price)
        self.assertEqual(
            response.json()[self.new_shipping_address_1.country]['count'], 2)
        self.assertEqual(response.json()[
                         self.new_shipping_address_2.country]['totalEarnings'], self.new_order_item_3.price)
        self.assertEqual(
            response.json()[self.new_shipping_address_2.country]['count'], 1)

    def test_get_total_earnings_by_country_same_country_different_orders(self):
        """Total earnings and count should depend on the name of the country not the order or shipping address"""
        self.new_shipping_address_2.country = self.new_shipping_address_1.country
        self.new_shipping_address_2.save()
        response = self.client.get(
            reverse('get-total-earnings-by-country'), **self.headers)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[self.new_shipping_address_1.country]['totalEarnings'],
                         self.new_order_item.price + self.new_order_item_2.price + self.new_order_item_3.price)
        self.assertEqual(
            response.json()[self.new_shipping_address_1.country]['count'], 3)

    def test_get_total_earnings_by_country_fails_no_staff(self):
        token = self.login_response_2.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        response = self.client.get(
            reverse('get-total-earnings-by-country'), **headers)

        self.assertEqual(response.status_code, 403)

    def test_get_total_earnings_by_country_fails_no_auth(self):
        response = self.client.get(
            reverse('get-total-earnings-by-country'))

        self.assertEqual(response.status_code, 401)

    def test_get_total_earnings_by_country_fails_wrong_method(self):
        post_response = self.client.post(
            reverse('get-total-earnings-by-country'), **self.headers)
        self.assertEqual(post_response.status_code, 405)

        put_response = self.client.put(
            reverse('get-total-earnings-by-country'), **self.headers)
        self.assertEqual(put_response.status_code, 405)

        patch_response = self.client.patch(
            reverse('get-total-earnings-by-country'), **self.headers)
        self.assertEqual(patch_response.status_code, 405)

        delete_response = self.client.delete(
            reverse('get-total-earnings-by-country'), **self.headers)
        self.assertEqual(delete_response.status_code, 405)


class TestGetAllPendingRequests(APITestCase):
    def setUp(self):
        self.email = 'test_user@gmail.com'
        self.password = 'a12341234'
        self.new_user = get_user_model().objects.create_user(email=self.email,
                                                             fullname='Test User', password=self.password,
                                                             is_active=True, is_staff=True)
        self.new_user_2 = get_user_model().objects.create_user(email='test_user2@gmail.com',
                                                               fullname='Test User', password=self.password,
                                                               is_active=True)

        login_response = self.client.post(reverse('token_obtain_pair'), data={
            'email': self.email, 'password': self.password})
        self.login_response_2 = self.client.post(reverse('token_obtain_pair'), data={
            'email': 'test_user2@gmail.com', 'password': self.password})

        self.token = login_response.json()['token']
        self.headers = {"HTTP_AUTHORIZATION": f'JWT {self.token}'}

        self.new_order_1 = Order.objects.create(user=self.new_user, paymentMethod='testmethod1',
                                                taxPrice=300, totalPrice=3350, shippingPrice=50, isPaid=True)

        self.new_order_2 = Order.objects.create(user=self.new_user, paymentMethod='testmethod2',
                                                taxPrice=50, totalPrice=1600, shippingPrice=50, isPaid=True)

        self.new_order_3 = Order.objects.create(user=self.new_user, paymentMethod='testmethod3',
                                                taxPrice=50, totalPrice=1800, shippingPrice=50)

    def test_get_all_pending_requests_route_success(self):
        response = self.client.get(
            reverse('get-all-pending-requests'), **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_all_pending_requests_success_content(self):
        response = self.client.get(
            reverse('get-all-pending-requests'), **self.headers)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(
            response.json()[0]['paymentMethod'], self.new_order_1.paymentMethod)
        self.assertEqual(
            response.json()[1]['paymentMethod'], self.new_order_2.paymentMethod)
        self.assertEqual(response.json()[0]['isPaid'], self.new_order_1.isPaid)
        self.assertEqual(response.json()[1]['isPaid'], self.new_order_2.isPaid)
        self.assertEqual(
            response.json()[0]['isDelivered'], self.new_order_1.isDelivered)
        self.assertEqual(
            response.json()[1]['isDelivered'], self.new_order_2.isDelivered)

    def test_get_all_pending_requests_change_is_paid(self):
        """Changing not paid and not delivered order to paid should add it to the response"""
        self.new_order_3.isPaid = True
        self.new_order_3.save()
        response = self.client.get(
            reverse('get-all-pending-requests'), **self.headers)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(
            response.json()[2]['paymentMethod'], self.new_order_3.paymentMethod)

    def test_get_all_pending_requests_change_is_delivered(self):
        """Changing paid and not delivered order to delivered should remove it from the response"""
        self.new_order_2.isDelivered = True
        self.new_order_2.save()
        response = self.client.get(
            reverse('get-all-pending-requests'), **self.headers)
        self.assertEqual(len(response.json()), 1)

    def test_get_all_pending_requests_fails_no_staff(self):
        token = self.login_response_2.json()['token']
        headers = {'HTTP_AUTHORIZATION': f'JWT {token}'}

        response = self.client.get(
            reverse('get-all-pending-requests'), **headers)

        self.assertEqual(response.status_code, 403)

    def test_get_all_pending_requests_fails_no_auth(self):
        response = self.client.get(
            reverse('get-all-pending-requests'))

        self.assertEqual(response.status_code, 401)

    def test_get_all_pending_requests_fails_wrong_method(self):
        post_response = self.client.post(
            reverse('get-all-pending-requests'), **self.headers)
        self.assertEqual(post_response.status_code, 405)

        put_response = self.client.put(
            reverse('get-all-pending-requests'), **self.headers)
        self.assertEqual(put_response.status_code, 405)

        patch_response = self.client.patch(
            reverse('get-all-pending-requests'), **self.headers)
        self.assertEqual(patch_response.status_code, 405)

        delete_response = self.client.delete(
            reverse('get-all-pending-requests'), **self.headers)
        self.assertEqual(delete_response.status_code, 405)
