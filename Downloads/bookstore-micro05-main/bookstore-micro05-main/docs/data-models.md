# Data Models

Each microservice owns its own isolated PostgreSQL database. Services do **not** share databases — they communicate via HTTP. Foreign keys between services are stored as plain integer IDs (no DB-level constraints across services).

---

## customer_db — Customer Service

### `Customer`

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | integer | PK, auto | Unique customer ID |
| `name` | varchar(255) | required | Full name |
| `email` | varchar | unique, required | Email address (used for login) |
| `password` | varchar(128) | required | Hashed password |

---

## book_db — Book Service

### `Book`

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | integer | PK, auto | Unique book ID |
| `title` | varchar(255) | required | Book title |
| `author` | varchar(255) | required | Author name |
| `picture_url` | URLField | blank, default='' | Cover image URL |
| `price` | decimal(10,2) | required | Selling price |
| `stock` | integer | required | Available quantity |
| `catalog_id` | integer | nullable | FK → Catalog.id (cross-service) |

---

## cart_db — Cart Service

### `Cart`

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | integer | PK, auto | Unique cart ID |
| `customer_id` | integer | required | FK → Customer.id (cross-service) |

### `CartItem`

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | integer | PK, auto | Unique item ID |
| `cart` | FK → Cart | CASCADE | Parent cart |
| `book_id` | integer | required | FK → Book.id (cross-service) |
| `quantity` | integer | required | Number of copies |

---

## staff_db — Staff Service

### `Staff`

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | integer | PK, auto | Unique staff ID |
| `name` | varchar(255) | required | Full name |
| `email` | varchar | unique | Login email |
| `password` | varchar(128) | required | Hashed password |

---

## manager_db — Manager Service

### `Manager`

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | integer | PK, auto | Unique manager ID |
| `name` | varchar(255) | required | Full name |
| `email` | varchar | unique | Login email |
| `password` | varchar(128) | required | Hashed password |

---

## catalog_db — Catalog Service

### `Catalog`

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | integer | PK, auto | Unique catalog ID |
| `name` | varchar(255) | required | Category name (e.g. "Manga", "Fiction") |

---

## order_db — Order Service

### `Order`

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | integer | PK, auto | Unique order ID |
| `customer_id` | integer | required | FK → Customer.id (cross-service) |
| `status` | varchar(50) | default='pending' | Order status |
| `total_amount` | decimal(10,2) | default=0 | Total order value |
| `created_at` | datetime | auto_now_add | Timestamp of creation |

**Status values:** `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`

### `OrderItem`

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | integer | PK, auto | Unique item ID |
| `order` | FK → Order | CASCADE | Parent order |
| `book_id` | integer | required | FK → Book.id (cross-service) |
| `quantity` | integer | required | Number of copies |
| `price` | decimal(10,2) | required | Unit price at time of order |

---

## ship_db — Ship Service

### `Shipment`

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | integer | PK, auto | Unique shipment ID |
| `order_id` | integer | required | FK → Order.id (cross-service) |
| `status` | varchar(50) | default='pending' | Shipment status |
| `address` | text | blank | Delivery address |

**Status values:** `pending`, `dispatched`, `in_transit`, `delivered`

---

## pay_db — Pay Service

### `Payment`

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | integer | PK, auto | Unique payment ID |
| `order_id` | integer | required | FK → Order.id (cross-service) |
| `amount` | decimal(10,2) | required | Payment amount |
| `status` | varchar(50) | default='pending' | Payment status |

**Status values:** `pending`, `completed`, `failed`, `refunded`

---

## comment_rate_db — Comment & Rate Service

### `Review`

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | integer | PK, auto | Unique review ID |
| `book_id` | integer | required | FK → Book.id (cross-service) |
| `customer_id` | integer | required | FK → Customer.id (cross-service) |
| `rating` | integer | required | Rating score (1–5) |
| `comment` | text | blank | Review text |

---

## recommender_db — Recommender AI Service

### `Recommendation`

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | integer | PK, auto | Unique recommendation ID |
| `customer_id` | integer | required | FK → Customer.id (cross-service) |
| `book_id` | integer | required | FK → Book.id (cross-service) |
| `score` | float | required | Recommendation confidence score (0–1) |

---

## Cross-Service Relationship Diagram

```
Customer ─────────────────────────────────────────────────┐
   │                                                       │
   ├──(customer_id)──► Cart ──(book_id)──► Book           │
   │                     └── CartItem                      │
   │                                                       │
   ├──(customer_id)──► Order ──(book_id)──► Book          │
   │                     │                                 │
   │                     ├──(order_id)──► Payment         │
   │                     └──(order_id)──► Shipment        │
   │                                                       │
   ├──(customer_id)──► Review ──(book_id)──► Book         │
   │                                                       │
   └──(customer_id)──► Recommendation ──(book_id)──► Book │

Book ──(catalog_id)──► Catalog
```

> Cross-service references are **soft foreign keys** (integer IDs only). Referential integrity is enforced at the application layer, not at the database level.
