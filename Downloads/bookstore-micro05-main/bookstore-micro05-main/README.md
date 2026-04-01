# Bookstore Microservices

A full-stack online bookstore built with a **microservices architecture** using Django REST Framework, PostgreSQL, and Docker. Includes a customer-facing shop and a staff/manager admin dashboard, all routed through a central API Gateway.

---

## Architecture Overview

```
                        ┌─────────────────────┐
                        │     API Gateway      │
                        │   (port 8000)        │
                        │  Django + Templates  │
                        └────────┬────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
   ┌────▼─────┐           ┌──────▼──────┐         ┌──────▼──────┐
   │ Customer │           │    Book     │          │   Catalog   │
   │ Service  │           │  Service   │          │   Service   │
   │ :8001    │           │   :8002    │          │   :8006     │
   └──────────┘           └─────────────┘         └─────────────┘
        │                        │                        │
   ┌────▼─────┐           ┌──────▼──────┐         ┌──────▼──────┐
   │   Cart   │           │    Order    │          │   Payment   │
   │ Service  │           │   Service  │          │   Service   │
   │  :8003   │           │   :8007    │          │   :8009     │
   └──────────┘           └─────────────┘         └─────────────┘
        │                        │                        │
   ┌────▼─────┐           ┌──────▼──────┐         ┌──────▼──────┐
   │Shipment  │           │  Comment &  │          │ Recommender │
   │ Service  │           │   Rating   │          │ AI Service  │
   │  :8008   │           │   :8010    │          │   :8011     │
   └──────────┘           └─────────────┘         └─────────────┘
        │
   ┌────▼─────┐   ┌──────────────┐
   │  Staff   │   │   Manager    │
   │ Service  │   │   Service   │
   │  :8004   │   │   :8005     │
   └──────────┘   └──────────────┘
```

---

## Services

| Service | Port | Description |
|---|---|---|
| **api-gateway** | 8000 | Central entry point, routes requests to all services |
| **customer-service** | 8001 | Customer registration, login, profile management |
| **book-service** | 8002 | Book catalog with cover images, stock, pricing |
| **cart-service** | 8003 | Shopping cart and cart item management |
| **staff-service** | 8004 | Staff account management |
| **manager-service** | 8005 | Manager/admin account management |
| **catalog-service** | 8006 | Book categories and catalog management |
| **order-service** | 8007 | Order creation, triggers payment and shipment |
| **ship-service** | 8008 | Shipment tracking and delivery management |
| **pay-service** | 8009 | Payment processing and records |
| **comment-rate-service** | 8010 | Book reviews and ratings |
| **recommender-ai-service** | 8011 | AI-based book recommendation engine |

---

## Tech Stack

- **Backend:** Django 4.x, Django REST Framework
- **Database:** PostgreSQL 15 (separate DB per service)
- **Containerization:** Docker, Docker Compose
- **Frontend:** Django Templates, Bootstrap 5
- **Auth:** Django session-based authentication

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Git

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Tusie69/bookstore-microservice.git
cd bookstore-microservice
```

### 2. Start all services

```bash
docker compose up -d --build
```

This will:
- Start a shared PostgreSQL 15 instance
- Initialize all 12 databases via `init-databases.sql`
- Build and start all 12 microservice containers

Wait ~30 seconds for all services to be healthy.

### 3. Seed sample data (optional)

```bash
docker compose exec api-gateway python /app/seed_data.py
```

Or run the seed script from the host:

```bash
pip install requests
python seed_data.py
```

---

## Usage

### Customer Shop

| URL | Description |
|---|---|
| `http://localhost:8000/` | Home page |
| `http://localhost:8000/books/` | Browse all books |
| `http://localhost:8000/books/<id>/` | Book detail page |
| `http://localhost:8000/cart/` | Shopping cart |
| `http://localhost:8000/checkout/` | Checkout |
| `http://localhost:8000/orders/` | My orders |
| `http://localhost:8000/register/` | Customer registration |
| `http://localhost:8000/login/` | Customer login |

### Staff / Manager Dashboard

| URL | Description |
|---|---|
| `http://localhost:8000/dashboard/login/` | Dashboard login |
| `http://localhost:8000/dashboard/` | Dashboard home |
| `http://localhost:8000/dashboard/books/` | Manage books |
| `http://localhost:8000/dashboard/orders/` | Manage orders |
| `http://localhost:8000/dashboard/customers/` | Manage customers |
| `http://localhost:8000/dashboard/payments/` | Manage payments |
| `http://localhost:8000/dashboard/shipments/` | Manage shipments |
| `http://localhost:8000/dashboard/catalogs/` | Manage catalogs |
| `http://localhost:8000/dashboard/reviews/` | Manage reviews |
| `http://localhost:8000/dashboard/staffs/` | Manage staff |
| `http://localhost:8000/dashboard/managers/` | Manage managers |

---

## Project Structure

```
bookstore-microservice/
├── docker-compose.yml          # Orchestrates all services
├── init-databases.sql          # Creates all PostgreSQL databases
├── seed_data.py                # Seeds sample books, customers, catalogs
├── api-gateway/                # Central gateway + frontend templates
│   ├── api_gateway/
│   │   ├── views.py            # Dashboard views
│   │   ├── shop_views.py       # Customer shop views
│   │   └── urls.py             # URL routing
│   └── templates/
│       ├── base.html
│       ├── home.html
│       ├── books.html
│       └── shop/               # Customer-facing templates
├── book-service/               # Book CRUD + picture_url
├── cart-service/               # Cart management
├── customer-service/           # Customer auth
├── order-service/              # Order processing
├── pay-service/                # Payments
├── ship-service/               # Shipments
├── catalog-service/            # Book categories
├── comment-rate-service/       # Reviews & ratings
├── recommender-ai-service/     # AI recommendations
├── staff-service/              # Staff management
└── manager-service/            # Manager management
```

---

## Development

### Rebuild a single service after code changes

```bash
docker compose up -d --build <service-name>
# Example:
docker compose up -d --build api-gateway
```

> **Note:** There are no volume mounts — every code change requires a rebuild to take effect.

### View logs

```bash
docker compose logs -f api-gateway
docker compose logs -f order-service
```

### Stop all services

```bash
docker compose down
```

### Reset everything (including database volumes)

```bash
docker compose down -v
```

---

## Notes

- Each microservice has its own isolated PostgreSQL database
- The API Gateway communicates with all services via internal HTTP calls
- Checkout is protected against double-submission with one-time session tokens
- Book cover images are stored as URLs (`picture_url`) in the book-service database
