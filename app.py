from __future__ import annotations

import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

from admin_panel import init_admin
from extensions import cors, db, jwt, limiter, migrate, socketio
from routes.analytics import analytics_bp
from routes.auth import auth_bp
from routes.categories import categories_bp
from routes.menu import menu_bp
from routes.orders import orders_bp
from routes.payments import payments_bp
from routes.receipts import receipts_bp
from routes.web import web_bp
from seed_data import seed_database

load_dotenv()


def _env_flag(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///restaurant.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-secret")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=14)
    app.config["RATELIMIT_DEFAULT"] = "200 per day;50 per hour"

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": os.getenv("CORS_ORIGINS", "*")}})
    limiter.init_app(app)
    socketio.init_app(app, async_mode=os.getenv("SOCKETIO_ASYNC_MODE", "eventlet"))

    app.register_blueprint(web_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(menu_bp, url_prefix="/api/menu")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(orders_bp, url_prefix="/api/orders")
    app.register_blueprint(payments_bp, url_prefix="/api/payments")
    app.register_blueprint(receipts_bp, url_prefix="/api/receipts")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
    init_admin(app)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(_error):
        return render_template("errors/500.html"), 500

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "restaurant-management-system"})

    with app.app_context():
        db.create_all()
        seed_database(db, update_existing=_env_flag("SEED_UPDATE_EXISTING", False))

    return app


app = create_app()


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)