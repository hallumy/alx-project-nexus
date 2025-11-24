🛒 E-Commerce Backend
Real-World Backend Engineering Application

This project simulates a real-world backend development environment focused on building a scalable, secure, and performant backend system for an e-commerce platform. It mirrors the workflows, challenges, and expectations of professional backend engineering teams.

📘 Overview

The E-Commerce Backend provides a robust API that powers an online product catalog. It includes secure user authentication, efficient product management, and advanced API features such as filtering, sorting, and pagination.

This case study prepares backend engineers to build production-ready systems using modern best practices.

🎯 Project Goals
1. CRUD APIs

Full CRUD support for:

Products

Categories

User accounts

JWT-based secure authentication & authorization.

2. Efficient Product Discovery

Filtering (category, price range, availability)

Sorting (price, date added, name)

Pagination (optimized for large datasets)

3. Database Optimization

Scalable relational schema design (PostgreSQL)

Query optimization and indexing for high-performance search

Real-world database structure design principles

🛠 Technologies Used
Technology	Purpose
Python	Core programming language
Django	Backend framework
Django REST Framework	API development
PostgreSQL	Relational database
JWT (SimpleJWT)	Token-based authentication
Swagger (drf-yasg)	API documentation
Django-Environ	Environment variable management
Docker	Containerization
CI/CD Pipelines	Automated build/testing

## Base URLs
* Service	URL
* REST API Root	http://localhost:8000/api/
* JWT Auth	http://localhost:8000/api/auth/jwt/
* Swagger Docs	http://localhost:8000/swagger/
* GraphQL API	http://localhost:8000/graphql/

## Authentication (JWT)

All authenticated REST requests require an access token.

Login (get JWT tokens)
`POST /api/auth/jwt/login/`
Body
'{
  "username": "example",
  "password": "password123"
}
`
Response
`{
  "refresh": "xxx",
  "access": "yyy"
}
`
Authorization Headers
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

## Database Schema

### User Table 

| Field       | Type     | Notes                       |
| ----------- | -------- | --------------------------- |
| id          | int (PK) | Auto-increment              |
| username    | varchar  | Unique                      |
| email       | varchar  | Unique                      |
| password    | varchar  | Hashed                      |
| first_name  | varchar  |                             |
| last_name   | varchar  |                             |
| phone       | varchar  | Optional                    |
| role        | varchar  | ("admin", "customer", Vendor) |
| date_joined | datetime | ISO format                  |

### Address Table 
| Field        | Type                | Notes                  |
| ------------ | ------------------- | ---------------------- |
| id           | int (PK)            |                        |
| user_id      | int (FK → users.id) |                        |
| street       | varchar             |                        |
| city         | varchar             |                        |
| region       | varchar             |                        |
| country      | varchar             |                        |
| postal_code  | varchar             |                        |
| address_type | varchar             | ("home", "work") |

### Product Table

| Field          | Type                   | Notes |
| -------------- | ---------------------- | ----- |
| id             | int (PK)               |       |
| category_id    | int (FK → category.id) |       |
| name           | varchar                |       |
| description    | text                   |       |
| price          | decimal                |       |
| stock_quantity | int                    |       |
| sku            | varchar                |       |
| brand          | varchar                |       |
| image_url      | varchar                |       |
| is_active      | boolean                |       |
| date_added     | datetime               |       |

### Product Variant Table
| Field        | Type                  | Notes                 |
| ------------ | --------------------- | --------------------- |
| id           | int (PK)              |                       |
| product_id   | int (FK → product.id) |                       |
| variant_name | varchar               | (e.g., "Red - Large") |
| sku          | varchar               | Unique                |
| price        | decimal               |                       |
| stock        | int                   |                       |
| image_url    | varchar               |                       |
| created_at   | datetime              |                       |
| updated_at   | datetime              |                       |

### Category Table

| Field       | Type                   | Notes                 |
| ----------- | ---------------------- | --------------------- |
| id          | int (PK)               |                       |
| name        | varchar                |                       |
| description | text                   |                       |
| parent_id   | int (nullable)         | For nested categories |
| created_at  | datetime                |                       |

### Cart Table

| Field      | Type                | Notes |
| ---------- | ------------------- | ----- |
| id         | int (PK)            |       |
| user_id    | int (FK → users.id) |       |
| created_at | datetime            |       |
| updated_at | datetime            |       |

### Cart Item Table

| Field      | Type                          | Notes          |
| ---------- | ----------------------------- | -------------- |
| id         | int (PK)                      |                |
| cart_id    | int (FK → cart.id)            |                |
| variant_id | int (FK → product_variant.id) |                |
| quantity   | int                           |                |
| price      | decimal                       | Snapshot price |
| created_at | datetime                      |                |
| updated_at | datetime                      |                |


### Order Table

| Field          | Type                  | Notes                     |
| -------------- | --------------------- | ------------------------- |
| id             | int (PK)              |                           |
| user_id        | int (FK → users.id)   |                           |
| address_id     | int (FK → address.id) |                           |
| order_number   | varchar               | Unique                    |
| total_amount   | decimal               |                           |
| payment_status | varchar               | ("paid", "pending", etc.) |
| order_date     | datetime              |                           |
| shipped_date   | datetime (nullable)   |                           |
| payment_method | varchar               |                           |


### Order Item Table

| Field      | Type                          | Notes            |
| ---------- | ----------------------------- | ---------------- |
| id         | int (PK)                      |                  |
| order_id   | int (FK → order.id)           |                  |
| variant_id | int (FK → product_variant.id) |                  |
| quantity   | int                           |                  |
| price      | decimal                       | Unit price       |
| subtotal   | decimal                       | price × quantity |

### Review Table

| Field      | Type                  | Notes |
| ---------- | --------------------- | ----- |
| id         | int (PK)              |       |
| user_id    | int (FK → users.id)   |       |
| product_id | int (FK → product.id) |       |
| rating     | int                   | 1–5   |
| comment    | text                  |       |
| created_at | datetime              |       |

### Wishlist Table

| Field      | Type                   | Notes |
| ---------- | ---------------------- | ----- |
| id         | int (PK)               |       |
| user_id    | int (FK → users.id)    |       |
| created_at | varchar (ISO datetime) |       |


### Wishlist Item Table

| Field       | Type                   | Notes |
| ----------- | ---------------------- | ----- |
| id          | int (PK)               |       |
| wishlist_id | int (FK → wishlist.id) |       |
| product_id  | int (FK → product.id)  |       |
| created_at  | datetime               |       |

### Payment Table

| Field               | Type                | Notes                   |
| ------------------- | ------------------- | ----------------------- |
| id                  | int (PK)            |                         |
| order_id            | int (FK → order.id) |                         |
| payment_method      | varchar             | ("card", "mpesa", etc.) |
| transaction_id      | varchar             |                         |
| amount              | decimal             |                         |
| phone_number        | varchar             | For mobile payments     |
| checkout_request_id | varchar             |                         |
| result_code         | varchar             |                         |
| result_description  | text                |                         |
| payment_status      | varchar             |                         |
| paid_at             | datetime            |                         |
| payment_date        | datetime            |                         |

### Discount Table

| Field            | Type                             | Notes |
| ---------------- | -------------------------------- | ----- |
| id               | int (PK)                         |       |
| code             | varchar                          |       |
| description      | varchar                          |       |
| discount_type    | varchar ("percentage" / "fixed") |       |
| discount_value   | varchar                          |       |
| minimum_purchase | decimal                          |       |
| maximum_discount | decimal                          |       |
| start_date       | datetime                         |       |
| end_date         | datetime                         |       |
| is_active        | boolean                          |       |

### Product Discount

| Field       | Type                  | Notes |
| ----------- | --------------------- | ----- |
| id          | int (PK)              |       |
| discount_id | int (FK)              |       |
| product_id  | int (FK → product.id) |       |

### Shipment Table

| Field           | Type                | Notes |
| --------------- | ------------------- | ----- |
| id              | int (PK)            |       |
| order_id        | int (FK → order.id) |       |
| tracking_number | varchar             |       |
| carrier         | varchar             |       |
| status          | varchar             |       |
| shipped_at      | datetime            |       |
| delivered_at    | datetime            |       |

