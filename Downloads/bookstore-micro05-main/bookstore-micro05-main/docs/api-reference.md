# API Reference

All services expose a REST API on their internal port. In local development, they are accessible directly via their mapped host ports. The API Gateway (`port 8000`) communicates with them internally via Docker networking.

> **Base URLs (local development):**
> - Prefix each service URL with `http://localhost:<port>`
> - All endpoints return/accept `application/json`

---

## Customer Service — `http://localhost:8001`

### `GET /customers/`
List all customers.

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  }
]
```

---

### `POST /customers/`
Register a new customer.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secret123"
}
```

**Response:** `201 Created` with customer object.

---

### `POST /customers/login/`
Authenticate a customer.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "secret123"
}
```

**Response:** `200 OK` with customer object, or `401 Unauthorized`.

---

### `GET /customers/<id>/`
Retrieve a customer by ID.

### `PUT /customers/<id>/`
Update a customer.

### `DELETE /customers/<id>/`
Delete a customer.

---

## Book Service — `http://localhost:8002`

### `GET /books/`
List all books.

**Query Parameters:**
| Param | Type | Description |
|---|---|---|
| `catalog_id` | int | Filter by catalog |

**Response:**
```json
[
  {
    "id": 1,
    "title": "One Piece Vol. 1",
    "author": "Eiichiro Oda",
    "picture_url": "https://example.com/cover.jpg",
    "price": "12.99",
    "stock": 50,
    "catalog_id": 3
  }
]
```

---

### `POST /books/`
Create a new book.

**Request Body:**
```json
{
  "title": "One Piece Vol. 1",
  "author": "Eiichiro Oda",
  "picture_url": "https://example.com/cover.jpg",
  "price": 12.99,
  "stock": 50,
  "catalog_id": 3
}
```

---

### `GET /books/<id>/`
Retrieve a book by ID.

### `PUT /books/<id>/`
Update a book.

### `DELETE /books/<id>/`
Delete a book.

---

## Cart Service — `http://localhost:8003`

### `POST /carts/`
Create a new cart for a customer.

**Request Body:**
```json
{
  "customer_id": 1
}
```

---

### `GET /carts/<customer_id>/`
Get a customer's cart with all items.

**Response:**
```json
{
  "id": 5,
  "customer_id": 1,
  "items": [
    {
      "id": 12,
      "book_id": 3,
      "quantity": 2
    }
  ]
}
```

---

### `GET /carts/info/<customer_id>/`
Get cart metadata (id, item count) for a customer.

---

### `POST /cart-items/`
Add an item to a cart.

**Request Body:**
```json
{
  "cart": 5,
  "book_id": 3,
  "quantity": 2
}
```

---

### `GET /cart-items/<id>/`
Retrieve a single cart item.

### `DELETE /cart-items/<id>/`
Remove an item from the cart.

---

## Staff Service — `http://localhost:8004`

### `GET /staffs/`
List all staff members.

### `POST /staffs/`
Create a new staff account.

**Request Body:**
```json
{
  "name": "Alice",
  "email": "alice@store.com",
  "password": "secret123"
}
```

### `POST /staffs/login/`
Authenticate a staff member.

**Request Body:**
```json
{
  "email": "alice@store.com",
  "password": "secret123"
}
```

### `GET /staffs/<id>/`
Retrieve a staff member by ID.

### `PUT /staffs/<id>/`
Update a staff member.

### `DELETE /staffs/<id>/`
Delete a staff member.

### `GET /staffs/books/`
List books managed by staff. (Staff-specific book view)

---

## Manager Service — `http://localhost:8005`

### `GET /managers/`
List all managers.

### `POST /managers/`
Create a new manager account.

**Request Body:**
```json
{
  "name": "Bob",
  "email": "bob@store.com",
  "password": "secret123"
}
```

### `GET /managers/<id>/`
Retrieve a manager by ID.

### `PUT /managers/<id>/`
Update a manager.

### `DELETE /managers/<id>/`
Delete a manager.

---

## Catalog Service — `http://localhost:8006`

### `GET /catalogs/`
List all book catalogs/categories.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Manga"
  }
]
```

### `POST /catalogs/`
Create a new catalog.

**Request Body:**
```json
{
  "name": "Manga"
}
```

### `GET /catalogs/<id>/`
Retrieve a catalog by ID.

### `PUT /catalogs/<id>/`
Update a catalog.

### `DELETE /catalogs/<id>/`
Delete a catalog.

---

## Order Service — `http://localhost:8007`

### `GET /orders/`
List all orders.

**Query Parameters:**
| Param | Type | Description |
|---|---|---|
| `customer_id` | int | Filter orders by customer |

**Response:**
```json
[
  {
    "id": 54,
    "customer_id": 1,
    "status": "pending",
    "total_amount": "25.98",
    "created_at": "2026-04-01T10:00:00Z",
    "items": [
      {
        "id": 101,
        "book_id": 3,
        "quantity": 2,
        "price": "12.99"
      }
    ]
  }
]
```

### `POST /orders/`
Create a new order. Also automatically creates a **Payment** and **Shipment** record.

**Request Body:**
```json
{
  "customer_id": 1,
  "total_amount": 25.98,
  "items": [
    {
      "book_id": 3,
      "quantity": 2,
      "price": 12.99
    }
  ]
}
```

**Response:** `201 Created` with the full order object including items.

> **Note:** Order creation triggers automatic calls to pay-service and ship-service to create corresponding records.

### `GET /orders/<id>/`
Retrieve an order by ID.

### `PUT /orders/<id>/`
Update order status.

### `DELETE /orders/<id>/`
Delete an order.

---

## Ship Service — `http://localhost:8008`

### `GET /shipments/`
List all shipments.

**Query Parameters:**
| Param | Type | Description |
|---|---|---|
| `order_id` | int | Filter by order |

**Response:**
```json
[
  {
    "id": 1,
    "order_id": 54,
    "status": "pending",
    "address": "123 Main St"
  }
]
```

### `POST /shipments/`
Create a new shipment.

**Request Body:**
```json
{
  "order_id": 54,
  "status": "pending",
  "address": "123 Main St"
}
```

### `GET /shipments/<id>/`
Retrieve a shipment by ID.

### `PUT /shipments/<id>/`
Update shipment status.

### `DELETE /shipments/<id>/`
Delete a shipment.

---

## Pay Service — `http://localhost:8009`

### `GET /payments/`
List all payments.

**Query Parameters:**
| Param | Type | Description |
|---|---|---|
| `order_id` | int | Filter by order |

**Response:**
```json
[
  {
    "id": 1,
    "order_id": 54,
    "amount": "25.98",
    "status": "pending"
  }
]
```

### `POST /payments/`
Create a payment record.

**Request Body:**
```json
{
  "order_id": 54,
  "amount": 25.98,
  "status": "pending"
}
```

### `GET /payments/<id>/`
Retrieve a payment by ID.

### `PUT /payments/<id>/`
Update payment status.

### `DELETE /payments/<id>/`
Delete a payment record.

---

## Comment & Rate Service — `http://localhost:8010`

### `GET /reviews/`
List all reviews.

### `POST /reviews/`
Submit a review for a book.

**Request Body:**
```json
{
  "book_id": 3,
  "customer_id": 1,
  "rating": 5,
  "comment": "Amazing manga!"
}
```

### `GET /reviews/<id>/`
Retrieve a review by ID.

### `PUT /reviews/<id>/`
Update a review.

### `DELETE /reviews/<id>/`
Delete a review.

### `GET /reviews/book/<book_id>/`
Get all reviews for a specific book.

**Response:**
```json
[
  {
    "id": 1,
    "book_id": 3,
    "customer_id": 1,
    "rating": 5,
    "comment": "Amazing manga!"
  }
]
```

---

## Recommender AI Service — `http://localhost:8011`

### `GET /recommendations/`
List all recommendations.

### `GET /recommendations/<customer_id>/`
Get recommendations for a specific customer.

**Response:**
```json
[
  {
    "id": 1,
    "customer_id": 1,
    "book_id": 7,
    "score": 0.95
  }
]
```

### `GET /recommendations/detail/<id>/`
Retrieve a single recommendation by ID.

### `GET /recommendations/generate/<customer_id>/`
Trigger AI recommendation generation for a customer.

**Response:** `200 OK` with list of generated recommendations.

---

## HTTP Status Codes

| Code | Meaning |
|---|---|
| `200 OK` | Success |
| `201 Created` | Resource created |
| `400 Bad Request` | Invalid input |
| `401 Unauthorized` | Authentication failed |
| `404 Not Found` | Resource not found |
| `500 Internal Server Error` | Server-side error |
