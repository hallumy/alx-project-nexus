🛒 E-Commerce Backend
Real-World Backend Engineering Application

This project simulates a real-world backend development environment focused on building a scalable, secure, and performant backend system for an e-commerce platform. It mirrors the workflows, challenges, and expectations of professional backend engineering teams.

📘 Overview

The E-Commerce Backend provides a robust API that powers an online product catalog. It includes secure user authentication, efficient product management, and advanced API features such as filtering, sorting, and pagination.

Project Goals
1. CRUD APIs

Full CRUD support for:

* Products

* Categories

* User accounts

* JWT-based secure authentication & authorization.

2. Efficient Product Discovery

* Filtering (category, price range, availability)

* Sorting (price, date added, name)

* Pagination (optimized for large datasets)

3. Database Optimization

* Scalable relational schema design (PostgreSQL)

* Query optimization and indexing for high-performance search

* Real-world database structure design principles

🛠 Technologies Used
## Technology	Purpose
* Python	Core programming language
* Django	Backend framework
* Django REST Framework	API development
* PostgreSQL	Relational database
* JWT (SimpleJWT)	Token-based authentication
* Swagger (drf-yasg)	API documentation
* Django-Environ	Environment variable management
* Docker	Containerization
* CI/CD Pipelines	Automated build/testing

## Base URLs
* Service	URL
* REST API Root	http://localhost:8000/api/
* JWT Auth	http://localhost:8000/api/auth/jwt/
* Swagger Docs	http://localhost:8000/swagger/
* GraphQL API	http://localhost:8000/graphql/

## DATABASE SCHEMA

### E-Commerce Backend Database Overview
1. Users

Stores user accounts: username, email, password, name, phone, role (customer/admin/vendor).

Used for authentication, profiles, and permissions.

2. Address

Stores user addresses (home/work).

Linked to Users via user_id.

Frontend uses this for checkout, shipping, and profile address management.

3. Products & Categories

Products: name, description, price, stock, SKU, brand, image, active status.

Categories: organize products; can be nested.

Product Variants: specific versions (size/color), linked to a product.

4. Cart & Cart Items

Cart: linked to a user.

Cart Items: each product variant in the cart with quantity and price.

Used for the shopping cart functionality.

5. Orders & Order Items

Orders: created when a user checks out; includes total, payment status, shipping address.

Order Items: specific product variants in an order, quantity, price.

Used to display order history, details, and track shipments.

6. Payments

Records payment transactions: method (card, mobile), amount, status, timestamps.

Used to confirm payment status and display transaction info.

7. Shipments

Tracks shipping for orders: carrier, tracking number, status, shipped/delivered dates.

Used to show shipment tracking to users.

8. Reviews

Users can review products: rating, comment, timestamp.

Linked to both Users and Products.

9. Wishlist & Wishlist Items

Users can save products for later.

Wishlist is linked to the user; wishlist items link to products.

10. Discounts & Product Discounts

Discounts (coupon codes) with type (percentage/fixed), value, validity.

Product discounts link specific discounts to products.

Relationships Summary

Users ↔ Address, Cart, Orders, Reviews, Wishlist

Products ↔ Categories, Product Variants, Reviews, Product Discounts

Cart ↔ Cart Items ↔ Product Variants

Orders ↔ Order Items ↔ Product Variants

Orders ↔ Payments, Shipments
 
Below is the ERD

![alt text](/image/ERD_ecom.png)


## Authentication (JWT)

All authenticated REST requests require an access token.

### Login (get JWT tokens)

`POST /api/auth/jwt/login/`
### Body
```json
{
  "username": "example",
  "password": "password123"
}
```

### Response
```json
{
  "refresh": "xxx",
  "access": "yyy"
}
```

### Authorization Headers
`Authorization: Bearer <access_token>`

## API Endpoints Summary

Below is a list of primary endpoints.

### Users

| Method | Endpoint                 | Description          |
| ------ | ------------------------ | -------------------- |
| POST   | `/api/auth/register/`    | Register user        |
| POST   | `/api/auth/jwt/login/`   | Login (JWT)          |
| POST   | `/api/auth/jwt/refresh/` | Refresh token        |
| GET    | `/api/auth/me/`          | Current user profile |
| GET    | `/api/users/`            | List users           |
| GET    | `/api/users/{id}/`       | Get user detail      |

### Address

| Method | Endpoint             |
| ------ | -------------------- |
| GET    | `/api/address/`      |
| POST   | `/api/address/`      |
| GET    | `/api/address/{id}/` |
| PATCH  | `/api/address/{id}/` |
| DELETE | `/api/address/{id}/` |

### Products
| Method | Endpoint              |
| ------ | --------------------- |
| GET    | `/api/product/`      |
| POST   | `/api/product/`      |
| GET    | `/api/product/{id}/` |
| PATCH  | `/api/product/{id}/` |
| DELETE | `/api/product/{id}/` |

### Product Variants

| Method | Endpoint              |
| ------ | --------------------- |
| GET    | `/api/variant/`      |
| POST   | `/api/variant/`      |
| GET    | `/api/variant/{id}/` |
| PATCH  | `/api/variant/{id}/` |
| DELETE | `/api/variant/{id}/` |

### Cart

| Method | Endpoint                      | Description             |
| ------ | ----------------------------- | ----------------------- |
| GET    | `/api/cart/`                  | Get current user's cart |
| POST   | `/api/cart/add/`              | Add variant to cart     |
| PATCH  | `/api/cart/update/{item_id}/` | Update quantity         |
| DELETE | `/api/cart/remove/{item_id}/` | Remove item             |

### Orders

| Method | Endpoint            |
| ------ | ------------------- |
| GET    | `/api/order/`      |
| POST   | `/api/order/`      |
| GET    | `/api/order/{id}/` |

Includes:

Items

Shipping address

Payment status

Shipment tracking

### Reviews

| Method | Endpoint             |
| ------ | -------------------- |
| GET    | `/api/review/`      |
| POST   | `/api/review/`      |
| GET    | `/api/review/{id}/` |

### Wishlist

| Method | Endpoint                          |
| ------ | --------------------------------- |
| GET    | `/api/wishlist/`                  |
| POST   | `/api/wishlist/add/`              |
| DELETE | `/api/wishlist/remove/{item_id}/` |

### Payments

| Method | Endpoint                           |
| ------ | ---------------------------------- |
| POST   | `/api/payment/initiate/`          |
| GET    | `/api/payment/{order_id}/status/` |

### Shipments

| Method | Endpoint                     |
| ------ | ---------------------------- |
| GET    | `/api/shipments/{order_id}/` |


## Instructions

### 1. **Create a Django Project**

#### Set up the Django Project
Create a new Django project named `ecommerce_app`.

    django-admin startproject ecommerce_app

Create an App within the Project

Inside the project, create an app named users:

    python manage.py startapp users

Install Necessary Packages

Install the required dependencies using pip.

    pip install django djangorestframework django-cors-headers celery rabbitmq drf-yasg

Make sure that you're in a virtual environment.

### 2. **Configure Settings**

#### Configure for REST Framework and CORS Headers

Open settings.py and add 'rest_framework' and 'corsheaders' to the INSTALLED_APPS:

    INSTALLED_APPS = [
        'rest_framework',
        'corsheaders',
        'users',
    ]

Add CORS middleware to the MIDDLEWARE list in settings.py:

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
    ]


Set up the Database Configuration for MySQL

Install mysqlclient for connecting to a Postgre database:

    pip install postgresql postgresql-contrib

Use the django-environ package to handle database credentials securely. Install django-environ:

    pip install django-dotenv

3. Add Swagger Documentation
Install drf-yasg

Install the drf-yasg package for Swagger API documentation:

    pip install drf-yasg

Configure Swagger for Auto Documentation

Open urls.py and add the following configuration to enable Swagger documentation:



3. Add Swagger Documentation
Install drf-yasg

Install the drf-yasg package for Swagger API documentation:

    pip install drf-yasg

Configure Swagger for Auto Documentation

Open urls.py and add the following configuration to enable Swagger documentation:

    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    from django.urls import path

    # Set up Swagger schema view
    schema_view = get_schema_view(
        openapi.Info(
            title="Alx Travel API",
            default_version='v1',
            description="API documentation for the Project",
            contact=openapi.Contact(email="contact@ecommerce.com"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    ]

This will make the Swagger UI available at http://localhost:8000/swagger/ once you run the server.

## Docker Setup (Containerization)

This project supports full Dockerization for local and production builds.

1. Dockerfile

``` FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "ecommerce_app.wsgi:application", "--bind", "0.0.0.0:8000"]
```

2. docker-compose.yml
``` version: "3.9"
services:
  db:
    image: "postgres:15-alpine"
    env_file: .env
    
  
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    env_file: .env
    container_name: "django_app"
    command: gunicorn ecommerce_app.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  redis:
    image: "redis:8-alpine"
    container_name: "redis_broker"
    ports:
      - "6379:6379"

  celery_worker:
    build: .
    container_name: "celery_worker"
    command: celery -A ecommerce_app worker --loglevel=info
    env_file: .env
    depends_on:
      - db
      - redis
    volumes:
      - .:/app

  celery_beat:
    build: .
    container_name: "celery_beat"
    command: celery -A ecommerce_app beat --loglevel=info
    env_file: .env
    depends_on:
      - db
      - redis
    volumes:
      - .:/app

  nginx:
    image: nginx:latest
    container_name: nginx_app
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
    ports:
      - "80:80"
    depends_on:
      - web
  

volumes:
  postgres_data:
  static_volume:
  media_volume:
```
## Jenkins CI/CD Pipeline

Below is a production-ready Jenkins pipeline.

Jenkinsfile
```
pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/your-repo/ecommerce-backend.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ecommerce-backend .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh '''
                docker login -u $DOCKER_USER -p $DOCKER_PASS
                docker tag ecommerce-backend $DOCKER_USER/ecommerce-backend:latest
                docker push $DOCKER_USER/ecommerce-backend:latest
                '''
            }
        }

        stage('Deploy to Heroku') {
            steps {
                sh '''
                heroku container:login
                heroku container:push web --app your-heroku-app
                heroku container:release web --app your-heroku-app
                '''
            }
        }
    }
}
```
## Heroku Deployment Guide
1. Install Heroku CLI
`curl https://cli-assets.heroku.com/install.sh | sh`

2. Login
`heroku login`

3. Create Heroku App
`heroku create ecommerce-backend-app`

4. Deploy via Docker
`heroku container:login`
`heroku container:push web --app ecommerce-backend-app`
`heroku container:release web --app ecommerce-backend-app`

5. Set Environment Variables
`heroku config:set SECRET_KEY=xxxx`
`heroku config:set DATABASE_URL=postgres://...`
