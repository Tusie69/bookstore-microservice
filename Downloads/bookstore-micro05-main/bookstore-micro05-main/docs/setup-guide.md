# Setup Guide

## Prerequisites

| Tool | Version | Install |
|---|---|---|
| Docker Desktop | 4.x+ | [docker.com](https://www.docker.com/products/docker-desktop/) |
| Docker Compose | bundled with Docker Desktop | — |
| Git | any | [git-scm.com](https://git-scm.com/) |
| Python | 3.10+ (optional, for running seed locally) | [python.org](https://www.python.org/) |

---

## 1. Clone the Repository

```bash
git clone https://github.com/Tusie69/bookstore-microservice.git
cd bookstore-microservice
```

---

## 2. Start All Services

```bash
docker compose up -d --build
```

This command will:
1. Pull PostgreSQL 15 image
2. Build all 12 service Docker images
3. Start the shared `db` container and wait for it to be healthy
4. Run `init-databases.sql` to create all 11 databases
5. Start all service containers
6. Start the API Gateway last

**First startup takes 2–5 minutes** depending on your machine and internet speed.

### Verify all containers are running

```bash
docker compose ps
```

You should see `21` containers with status `running` or `healthy`.

---

## 3. Run Migrations

Migrations run automatically via each service's `Dockerfile` entrypoint. If a service fails to migrate, run manually:

```bash
docker compose exec book-service python manage.py migrate
docker compose exec customer-service python manage.py migrate
# Repeat for any service that failed
```

---

## 4. Seed Sample Data (Recommended)

The seed script creates:
- Book catalogs (Manga, Fiction, Science, etc.)
- 99 sample books with cover images
- Sample customers
- Sample staff and manager accounts

```bash
pip install requests   # if running from host
python seed_data.py
```

Or run from inside the container:

```bash
docker compose exec api-gateway python /app/seed_data.py
```

> Re-running the seed script will create duplicate entries. Reset the database first if you want a clean slate (see [Reset](#reset-everything)).

---

## 5. Access the Application

| URL | Description |
|---|---|
| `http://localhost:8000/` | Customer shop home page |
| `http://localhost:8000/books/` | Browse all books |
| `http://localhost:8000/register/` | Customer registration |
| `http://localhost:8000/login/` | Customer login |
| `http://localhost:8000/dashboard/login/` | Staff / Manager dashboard login |
| `http://localhost:8000/dashboard/` | Admin dashboard |

---

## Development Workflow

### Making code changes

Since there are **no volume mounts**, every code change requires a rebuild of the affected service:

```bash
# Rebuild a single service (fastest)
docker compose up -d --build api-gateway

# Rebuild multiple services
docker compose up -d --build book-service order-service

# Rebuild everything
docker compose up -d --build
```

### Viewing logs

```bash
# Follow logs for one service
docker compose logs -f api-gateway

# View last 50 lines
docker compose logs --tail=50 order-service

# All services
docker compose logs -f
```

### Running Django shell

```bash
docker compose exec book-service python manage.py shell
```

### Running a management command

```bash
docker compose exec book-service python manage.py migrate
docker compose exec book-service python manage.py showmigrations
```

### Accessing PostgreSQL directly

```bash
docker compose exec db psql -U postgres -d book_db
```

---

## Stopping Services

### Stop all containers (keep data)

```bash
docker compose down
```

### Start again without rebuilding

```bash
docker compose up -d
```

---

## Reset Everything

> **Warning:** This deletes all data including the database volume.

```bash
docker compose down -v
docker compose up -d --build
python seed_data.py
```

---

## Troubleshooting

### A service exits immediately on startup

Check logs for the failing service:

```bash
docker compose logs <service-name>
```

Common causes:
- Database not ready yet → wait a few seconds and retry, or check `db` healthcheck
- Migration error → run `docker compose exec <service> python manage.py migrate` manually

### Port already in use

If port 8000 (or any other port) is taken by another process:

```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace <PID> with actual PID)
taskkill /PID <PID> /F
```

### Images not loading (404 / 403)

The project uses `dummyimage.com` and `placehold.co` for placeholder images. These require an internet connection from the Docker container.

If images fail to load from inside the container, use any publicly accessible image URLs when updating `picture_url` in the database.

### Duplicate orders on checkout

This was fixed with a one-time session token implemented in `api-gateway/api_gateway/shop_views.py`. If the issue reoccurs, clear your browser session or cookies and try again.

### Duplicate catalog/book entries

If you've run `seed_data.py` multiple times, you may have duplicate catalog entries. Reset the database (see above) and seed once cleanly.

---

## Environment Variables

All environment variables are set in `docker-compose.yml`. The defaults use `postgres` as both the user and password (suitable for local development only).

| Variable | Default | Description |
|---|---|---|
| `DB_NAME` | varies per service | PostgreSQL database name |
| `DB_USER` | `postgres` | Database user |
| `DB_PASSWORD` | `postgres` | Database password |
| `DB_HOST` | `db` | Database hostname (Docker service name) |
| `DB_PORT` | `5432` | Database port |

> For production, replace these with environment-specific secrets and never commit credentials to version control.

---

## Service Port Reference

| Service | Host Port | Internal Port |
|---|---|---|
| api-gateway | 8000 | 8000 |
| customer-service | 8001 | 8000 |
| book-service | 8002 | 8000 |
| cart-service | 8003 | 8000 |
| staff-service | 8004 | 8000 |
| manager-service | 8005 | 8000 |
| catalog-service | 8006 | 8000 |
| order-service | 8007 | 8000 |
| ship-service | 8008 | 8000 |
| pay-service | 8009 | 8000 |
| comment-rate-service | 8010 | 8000 |
| recommender-ai-service | 8011 | 8000 |
| PostgreSQL | 5432 | 5432 |
