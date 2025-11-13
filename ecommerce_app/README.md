#  Ecommerce App Setup Guide

##  Objective
This guide outlines the steps to set up a Django project for the **Ecommerce App** with the necessary dependencies, configure the **PostgreSQL** database, and add **Swagger** for API documentation.

---

##  1. Create a Django Project

###  Set up the Django Project
Create a new Django project named **ecommerce_app**:

```bash
django-admin startproject ecommerce_app

 Create an App within the Project

Inside the ecommerce_app project, create an app named users (or any core app):

cd ecommerce_app
python manage.py startapp users

## 2.Install Necessary packages

Install the required dependencies:

pip install django djangorestframework django-cors-headers django-environ psycopg2-binary drf-yasg

Explanation:

    django → Core framework

    djangorestframework → REST API support

    django-cors-headers → Handle cross-origin requests

    django-environ → Manage environment variables securely

    psycopg2-binary → PostgreSQL adapter

    drf-yasg → Swagger documentation generator

 Tip: Always use a virtual environment:

python -m venv venv
source venv/bin/activate

## 3. Configure Settings
Add REST Framework and CORS Headers

In ecommerce_app/settings.py, add the following to INSTALLED_APPS:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'users',  # Custom app
]

Add CORS Middleware

Add the middleware near the top of the list in settings.py:

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

Allow all origins during development:

CORS_ALLOW_ALL_ORIGINS = True

4. Configure the PostgreSQL Database
Install PostgreSQL Adapter

If not already installed:

pip install psycopg2-binary

Use django-environ for Environment Variables

At the top of settings.py:

import environ
import os

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

Database Configuration

Update the DATABASES section:

DATABASES = {
    'default': env.db(default='postgres://dbuser:dbpassword@localhost:5432/ecommerce_db')
}

Create a .env file in your project root:

DEBUG=True
DATABASE_URL=postgres://your_db_user:your_db_password@localhost:5432/ecommerce_db
SECRET_KEY=your_secret_key_here

## 5.Add Swagger Documentation

Install drf-yasg (if not already installed):

pip install drf-yasg

Configure Swagger

In your main ecommerce_app/urls.py, add the following:

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Ecommerce API",
        default_version='v1',
        description="API documentation for the Ecommerce App",
        contact=openapi.Contact(email="support@ecommerce.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),  # Include your app URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
]

Once your server runs, Swagger UI will be available at:
http://localhost:8000/swagger/
6. Run the Application

Apply migrations and start the server:

python manage.py makemigrations
python manage.py migrate
python manage.py runserver