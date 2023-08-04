# Ecommerce Website Project - Backend

### Description

Server side and API of ecommerce website project(Prime Connect). This project was build with Django and Django REST Framework.
This website has all the features that an ecommerce website needs. All the sales statistics is available to be used on frontend for charts and ... .

Keep in mind that adding a real payment method(like paypal api) was not possible because of limitaions i have in my country, because of that i only used a frontend package called "validator" to check if the credit card information is valid.


### Features

- For production, a react app is rendered by django as a single html file.
- For storing media files, cloudinary service was used.
- For the login process, access and refresh token method was used.
- Users have to provide an email, fullname and password to sign up to the website.
- For adding a lazy load feature to the website, a hash is created for each image(blurhash), this hash can be decoded on frontend and the result is a low quality version of the actual image, which i found is more efficient than storing thumbnail for product images.
- Admins can create new products, edit their information and delete them if needed.
- Admins can send each other messages if they want (This is not a chat application.) Once an admin checks a new message a field called is_read will change to True, It is possible for admins to set it to False again. Admins can see the messages they have sent and received separately, they can also delete the messages.
- Admins can also see all the admins in the website.
- There are Categories that can have several Sub Categories connected to them, each product is connected to one sub category.
- Admins have access to information about total monthly sales, annual sales, sales based on country, category and ... in their dashboard.
- For each product, there is a name, image, description, more details (for adding more info with pictures and ...), discount section, stock count section and a review-rating system. three images can be added for displaying one product,
However one is required. As mentioned before for each image there is a hashed value in the database.
- Customers can order products based on alphabetical order, price, rating and when they were added (old/new).
- Customers can filter products based on their brand, sub category, category and if they have discount or not.
- Customers can search for products based on their brand, sub category, category and if they have discount or not.
- Customers can search, filter and order products at the same time.
- Customers can buy several products at the same time, however they don't pay right away. They have the time to check their order, contact an admin if they have an issue or if they want it removed. They can pay for their order and this will add their order to the packages that have to be delivered, If delivery was successful, An admin will change status of the order to delivered.
- Customers can write their opinion about products and rate them.
- Customers and admins can reset their password using their emails.

### Technologies and libraries used

- Django
- Django REST framework
- Django filters
- Django REST framework simple jwt
- Django cors headers
- Blurhash
- blurhash-python
- Postgres
- psycopg2
- dj-database-url
- Cloudinary
- Django cloudinary storage
- Django white noise
- Pillow
- gunicorn
- python-dotenv

### How to run the project

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Ali-Fattahian/Ecommerce-Website-Prime-Connect.git
```

Create a virtual environment to install dependencies in and activate it:

```sh
python3 -m venv env
source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment.

Since this project is in production, you have to change settings to dev to work with it, so open settings.py,

Use an online tool like *https://djecrety.ir/*
to get a new secret key for the project.

Set DEBUG=True,

Create a database and set DATABASES settings to the one you created,

either remove cloudinary settings and apps from installed_apps or set the configuration to your own account, at last set the email config to your email.

once you did all of that,

```sh
python manage.py makemigrations
python manage.py migrate
```

To create the tables in your database.


```ssh
python manage.py runserver
```

to run the server.

You can navigate to
`http://localhost:8000/api/products/`
`http://localhost:8000/api/orders/`
`http://localhost:8000/api/users/`
to access the api routes

If you navigate to
`http://localhost:8000`
you access the react app that is working as a single page (index.html) rendered by django.

To run the tests,
`python manage.py tests`
