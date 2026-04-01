# Architecture

## Overview

This project follows a **microservices architecture** pattern where each business domain is implemented as an independent Django service with its own PostgreSQL database. All user-facing traffic flows through a central **API Gateway**.

---

## Architecture Pattern

```
Browser / Client
       │
       ▼
┌──────────────────────────────────────────────────┐
│                  API Gateway :8000               │
│                                                  │
│  ┌─────────────────┐   ┌───────────────────────┐ │
│  │  Customer Shop  │   │  Staff/Manager        │ │
│  │  (shop_views.py)│   │  Dashboard (views.py) │ │
│  └────────┬────────┘   └───────────┬───────────┘ │
│           │                        │             │
│           └──────────┬─────────────┘             │
│                      │ HTTP / _safe_get / _safe_post │
└──────────────────────┼──────────────────────────┘
                       │
     ┌─────────────────┼──────────────────────┐
     │                 │                      │
     ▼                 ▼                      ▼
Customer-svc      Book-svc              Catalog-svc
  :8001             :8002                 :8006
     │                 │                      │
     ▼                 ▼                      ▼
customer_db       book_db               catalog_db

     │                 │
     ▼                 ▼
  Cart-svc         Order-svc ──────► Pay-svc :8009
   :8003             :8007    │           │
     │                 │      │       pay_db
     ▼                 ▼      │
  cart_db          order_db   └──────► Ship-svc :8008
                                            │
                                        ship_db
     │
     ▼
Comment-Rate-svc                 Recommender-AI-svc
    :8010                              :8011
     │                                    │
comment_rate_db                    recommender_db
```

---

## Design Principles

### 1. Database per Service
Each service owns exactly one PostgreSQL database. No service reads or writes another service's database directly.

```
customer-service  →  customer_db
book-service      →  book_db
cart-service      →  cart_db
staff-service     →  staff_db
manager-service   →  manager_db
catalog-service   →  catalog_db
order-service     →  order_db
ship-service      →  ship_db
pay-service       →  pay_db
comment-rate-svc  →  comment_rate_db
recommender-svc   →  recommender_db
```

### 2. API Gateway as Single Entry Point
The API Gateway (`port 8000`) is the only service exposed to the browser. It:
- Renders Django templates for both the customer shop and admin dashboard
- Aggregates data from multiple services via internal HTTP calls
- Handles session-based authentication
- Never bypasses services to access databases directly

### 3. Synchronous HTTP Communication
Services communicate via synchronous REST HTTP calls. The gateway uses helper functions:
- `_safe_get(url)` — GET with error handling, returns `[]` or `{}` on failure
- `_safe_post(url, data)` — POST with JSON body, returns response or `None`

### 4. Soft Foreign Keys
Cross-service references (e.g. `customer_id` in an Order) are stored as plain integers. There are no database-level foreign key constraints across service boundaries.

### 5. Event-Driven Side Effects (Inline)
When an Order is created, the order-service automatically calls pay-service and ship-service to create corresponding Payment and Shipment records in the same request cycle. This is a simplified synchronous pattern (not true async event sourcing).

---

## Key Flows

### Customer Checkout Flow

```
1. Customer adds book to cart
   GET /books/<id>/  →  book-service
   POST /cart-items/ →  cart-service

2. Customer views cart
   GET /carts/<customer_id>/ →  cart-service
   GET /books/<id>/           →  book-service (for each item)

3. Customer places order (checkout)
   a. Gateway generates one-time checkout_token → stores in session
   b. On form submit: validates token (prevents double-submit)
   c. POST /orders/  →  order-service
      └─ order-service POST /payments/ →  pay-service  (auto)
      └─ order-service POST /shipments/ →  ship-service (auto)
   d. DELETE /cart-items/<id>/ → cart-service (clears cart)
   e. Token consumed from session
```

### Staff Dashboard Data Flow

```
1. Staff logs in
   POST /staffs/login/ → staff-service

2. Dashboard loads books
   GET /books/    → book-service
   GET /catalogs/ → catalog-service (for filter options)

3. Dashboard loads orders
   GET /orders/     → order-service
   GET /customers/  → customer-service (to resolve customer names)

4. Dashboard manages payments/shipments
   GET /payments/  → pay-service
   GET /shipments/ → ship-service
```

---

## Service Responsibilities

| Service | Owns | Does NOT own |
|---|---|---|
| customer-service | Customer accounts, auth | Sessions (managed by gateway) |
| book-service | Book data, stock, cover images | Catalog names (just stores catalog_id) |
| cart-service | Cart and CartItem records | Book details (just stores book_id) |
| order-service | Orders, OrderItems | Payment processing, shipment tracking |
| pay-service | Payment records | Order business logic |
| ship-service | Shipment records | Logistics integration |
| catalog-service | Category definitions | Book assignments |
| comment-rate-service | Reviews, ratings | Customer/book details |
| recommender-ai-service | Recommendation scores | ML model training infra |
| staff-service | Staff accounts | Book management (delegated) |
| manager-service | Manager accounts | Role enforcement |
| api-gateway | Routing, rendering, auth sessions | All domain data |

---

## Infrastructure

### Docker Compose
All services are defined in `docker-compose.yml`. They share a single Docker network and communicate by container name (e.g. `http://customer-service:8000`).

```yaml
services:
  db:              # Shared PostgreSQL instance, multiple databases
  customer-service: # :8001
  book-service:    # :8002
  cart-service:    # :8003
  ...
  api-gateway:     # :8000 — depends on all services
```

### Database Initialization
`init-databases.sql` creates all 11 PostgreSQL databases when the `db` container starts for the first time:

```sql
CREATE DATABASE customer_db;
CREATE DATABASE book_db;
CREATE DATABASE cart_db;
-- ... etc
```

### No Volume Mounts for Code
Code changes require a container rebuild:
```bash
docker compose up -d --build <service-name>
```

---

## Security Notes

- Passwords are stored hashed in each service's database
- Session tokens are managed server-side by Django's session framework in the API Gateway
- Checkout uses a one-time CSRF-like token to prevent double order submission
- Cross-service calls happen on the internal Docker network (not exposed externally)
- No JWT or OAuth is implemented — this is a demo/educational project
