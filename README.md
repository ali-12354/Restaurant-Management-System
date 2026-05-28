# Harvest Table Restaurant Management System

A Flask-based restaurant management system with a single project tree, server-rendered pages, SQLite data, JWT API routes, live order updates, and printable receipts.

## What is included

- Public restaurant pages built with Flask templates and custom CSS
- REST API for auth, menu, categories, orders, payments, receipts, and analytics
- SQLite + SQLAlchemy models with seed data
- JWT auth, rate limiting, CORS, and Socket.IO wiring
- Docker and Docker Compose for local startup

## Local setup

1. Create a virtual environment.
2. Install dependencies from `requirements.txt`.
3. Copy `.env.example` to `.env` and adjust values if needed.
4. Run the app with `python app.py`.

Admin seed account:

- Email: `admin@restaurant.local`
- Password: `Admin@12345`

## API highlights

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/menu`
- `POST /api/orders`
- `GET /api/receipts/<order_id>`

## Notes

Stripe, Cloudinary, and production-grade webhooks are scaffolded as integration points, but the project currently uses local demo behavior so the app remains easy to run.

On startup, seed data is inserted only for missing records by default, so admin edits (for example dish image changes) are preserved across restarts. If you want startup seeding to overwrite existing seeded menu records, set `SEED_UPDATE_EXISTING=true` in your environment.