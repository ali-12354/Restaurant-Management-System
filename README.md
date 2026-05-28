# Restaurant-Management-System
Harvest Table: A Full-Stack Restaurant Management System I've built a comprehensive restaurant management system using Flask, SQLite, and modern web technologies.
Core Features:
 Complete Order Management – From menu browsing to checkout, payment processing, and printable receipts
 REST API – JWT authentication, secure endpoints for orders, payments, analytics, and menu management
 Admin Dashboard – Manage menu items, categories, orders, users, and view key metrics
 Real-time Updates – Socket.IO integration for live order notifications
 Responsive Frontend – Server-rendered templates with custom CSS and vanilla JavaScript
Tech Stack:
- Backend: Flask with SQLAlchemy ORM
- Database: SQLite with seeded demo data
- API: RESTful endpoints with JWT & rate limiting, CORS support
- Frontend: Jinja2 templates, responsive design
- DevOps: Docker & Docker Compose for easy deployment
- Additional: Socket.IO for live updates, payment scaffolding for Stripe/Cloudinary integration
Key Highlights:
• Non-destructive seeding – preserves admin edits across restarts
• Production-ready structure with proper authentication & authorization
• Cart management with localStorage persistence
• Admin seed account included for immediate testing
• Modular route structure for easy maintenance & scaling 
