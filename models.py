from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON
from sqlalchemy.orm import relationship

from extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="customer", nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")


class Category(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    items = relationship("MenuItem", back_populates="category")


class MenuItem(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    prep_time = db.Column(db.Integer, default=20, nullable=False)
    tags = db.Column(JSON, default=list, nullable=False)
    rating = db.Column(db.Float, default=4.5, nullable=False)

    category = relationship("Category", back_populates="items")
    order_items = relationship("OrderItem", back_populates="menu_item")


class Order(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    status = db.Column(db.String(40), default="Placed", nullable=False)
    total = db.Column(db.Float, default=0.0, nullable=False)
    payment_method = db.Column(db.String(30), default="cod", nullable=False)
    payment_status = db.Column(db.String(30), default="pending", nullable=False)
    delivery_address = db.Column(JSON, default=dict, nullable=False)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False, cascade="all, delete-orphan")
    receipt = relationship("Receipt", back_populates="order", uselist=False, cascade="all, delete-orphan")


class OrderItem(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_item.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")


class Payment(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False, unique=True)
    method = db.Column(db.String(30), nullable=False)
    stripe_intent_id = db.Column(db.String(255), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), default="pending", nullable=False)

    order = relationship("Order", back_populates="payment")


class Receipt(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False, unique=True)
    pdf_url = db.Column(db.String(500), nullable=True)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    order = relationship("Order", back_populates="receipt")


class ContactMessage(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    is_resolved = db.Column(db.Boolean, default=False, nullable=False)