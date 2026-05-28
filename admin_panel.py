from __future__ import annotations

import ast
import json

from flask import redirect, request, session, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.validators import Unique
from markupsafe import Markup
from sqlalchemy import func
from werkzeug.security import generate_password_hash
from wtforms import PasswordField, TextAreaField, ValidationError

from extensions import db
from models import Category, ContactMessage, MenuItem, Order, OrderItem, Payment, Receipt, User

# Patch WTForms Select widget to accept 3-tuple or 4-tuple choices.
try:
    from wtforms.widgets.core import Select as _WTSelect
    from wtforms.widgets.core import html_params

    def _patched_select_call(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        if self.multiple:
            kwargs["multiple"] = True
        flags = getattr(field, "flags", {})
        for k in dir(flags):
            if k in self.validation_attrs and k not in kwargs:
                kwargs[k] = getattr(flags, k)
        select_params = html_params(name=field.name, **kwargs)
        html = [f"<select {select_params}>"]
        if field.has_groups():
            for group, choices in field.iter_groups():
                optgroup_params = html_params(label=group)
                html.append(f"<optgroup {optgroup_params}>")
                for choice in choices:
                    try:
                        val, label, selected, render_kw = choice
                    except ValueError:
                        val, label, selected = choice
                        render_kw = {}
                    html.append(self.render_option(val, label, selected, **render_kw))
                html.append("</optgroup>")
        else:
            for choice in field.iter_choices():
                try:
                    val, label, selected, render_kw = choice
                except ValueError:
                    val, label, selected = choice
                    render_kw = {}
                html.append(self.render_option(val, label, selected, **render_kw))
        html.append("</select>")
        return Markup("".join(html))

    # Apply the patch
    _WTSelect.__call__ = _patched_select_call
except Exception:
    # If patch fails, best-effort continue; environment may differ.
    pass


if isinstance(Unique.field_flags, tuple):
    Unique.field_flags = {flag: True for flag in Unique.field_flags}


class SecureModelView(ModelView):
    can_export = True
    page_size = 25

    def is_accessible(self):
        return session.get("role") == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("web.login_page", next=request.url))


class OrderAdminView(SecureModelView):
    column_list = [
        "id",
        "status",
        "payment_status",
        "payment_method",
        "total",
        "user",
        "created_at",
    ]
    column_filters = ["status", "payment_status", "payment_method", "created_at"]
    column_searchable_list = ["id"]
    can_create = True
    can_delete = False
    column_default_sort = ("created_at", True)
    column_editable_list = ["status", "payment_status"]
    form_columns = [
        "status",
        "payment_status",
        "payment_method",
        "total",
        "delivery_address",
    ]
    form_overrides = {
        "delivery_address": TextAreaField,
    }

    def on_model_change(self, form, model, is_created):
        if isinstance(model.delivery_address, str):
            payload = model.delivery_address.strip()
            if not payload:
                model.delivery_address = {}
                return
            # Try JSON first
            try:
                model.delivery_address = json.loads(payload)
                return
            except json.JSONDecodeError:
                pass
            # Then try Python literal (dict)
            try:
                parsed = ast.literal_eval(payload)
                if isinstance(parsed, dict):
                    model.delivery_address = parsed
                    return
            except Exception:
                pass
            # Try simple key:value lines or key=value pairs
            parsed = {}
            for line in payload.splitlines():
                if ':' in line:
                    k, v = line.split(':', 1)
                    parsed[k.strip()] = v.strip()
                elif '=' in line:
                    k, v = line.split('=', 1)
                    parsed[k.strip()] = v.strip()
            if parsed:
                model.delivery_address = parsed
                return
            # Fallback: store the raw text as a single address line
            model.delivery_address = {"line1": payload}


class MenuItemAdminView(SecureModelView):
    column_list = [
        "id",
        "name",
        "category",
        "price",
        "rating",
        "is_available",
        "is_featured",
        "image_url",
        "updated_at",
    ]
    column_filters = ["category", "is_available", "is_featured", "updated_at"]
    column_searchable_list = ["name", "description"]
    column_default_sort = ("updated_at", True)
    form_columns = [
        "name",
        "description",
        "price",
        "category_id",
        "image_url",
        "is_available",
        "is_featured",
        "prep_time",
        "rating",
        "tags",
    ]
    form_overrides = {
        "tags": TextAreaField,
    }

    def _image_thumb(self, _context, _model, name):
        image_url = getattr(_model, name)
        if not image_url:
            return "-"
        return Markup(f'<img src="{image_url}" style="height:44px;width:72px;object-fit:cover;border-radius:8px;" alt="thumb">')

    column_formatters = {
        "image_url": _image_thumb,
    }

    def on_model_change(self, form, model, is_created):
        if isinstance(model.tags, str):
            payload = model.tags.strip()
            if not payload:
                model.tags = []
                return
            if payload.startswith("["):
                try:
                    parsed = json.loads(payload)
                except json.JSONDecodeError:
                    try:
                        parsed = ast.literal_eval(payload)
                    except (ValueError, SyntaxError) as exc:
                        raise ValidationError("Tags must be comma separated or a valid JSON list.") from exc
                if not isinstance(parsed, list):
                    raise ValidationError("Tags JSON must be a list.")
                model.tags = [str(tag).strip() for tag in parsed if str(tag).strip()]
                return
            model.tags = [tag.strip() for tag in payload.split(",") if tag.strip()]


class ContactMessageAdminView(SecureModelView):
    column_list = ["id", "name", "email", "subject", "is_read", "is_resolved", "created_at"]
    column_filters = ["is_read", "is_resolved", "created_at"]
    column_searchable_list = ["name", "email", "subject", "message"]
    form_columns = ["name", "email", "subject", "message", "is_read", "is_resolved"]
    can_create = False


class UserAdminView(SecureModelView):
    column_list = ["id", "name", "email", "role", "phone", "is_active", "created_at"]
    column_filters = ["role", "is_active", "created_at"]
    column_searchable_list = ["name", "email", "phone"]
    form_columns = ["name", "email", "password_hash", "role", "phone", "is_active"]
    form_overrides = {
        "password_hash": PasswordField,
    }
    form_args = {
        "password_hash": {
            "label": "Password",
            "description": "Leave empty on edit to keep the existing password.",
        },
    }

    def on_model_change(self, form, model, is_created):
        password = (model.password_hash or "").strip()
        if is_created and not password:
            raise ValidationError("Password is required when creating a user.")
        if not is_created and not password:
            original = User.query.get(model.id)
            model.password_hash = original.password_hash if original else ""
            return
        if password:
            model.password_hash = generate_password_hash(password)


class DashboardIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if session.get("role") != "admin":
            return redirect(url_for("web.login_page", next=request.url))

        total_orders = db.session.query(func.count(Order.id)).scalar() or 0
        revenue = db.session.query(func.coalesce(func.sum(Order.total), 0)).scalar() or 0
        pending_orders = db.session.query(func.count(Order.id)).filter(Order.status != "Delivered").scalar() or 0
        active_users = db.session.query(func.count(User.id)).filter(User.is_active.is_(True)).scalar() or 0

        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(6).all()
        message_count = db.session.query(func.count(ContactMessage.id)).filter(ContactMessage.is_read.is_(False)).scalar() or 0

        return self.render(
            "admin/index.html",
            stats={
                "total_orders": total_orders,
                "revenue": revenue,
                "pending_orders": pending_orders,
                "active_users": active_users,
                "unread_messages": message_count,
            },
            recent_orders=recent_orders,
        )


def init_admin(app):
    admin = Admin(
        app,
        name="Harvest Table Admin",
        index_view=DashboardIndexView(url="/admin", name="Dashboard"),
        base_template="admin/custom_master.html",
        template_mode="bootstrap4",
    )

    admin.add_view(MenuItemAdminView(MenuItem, db.session, category="Catalog"))
    admin.add_view(SecureModelView(Category, db.session, category="Catalog"))
    admin.add_view(OrderAdminView(Order, db.session, category="Operations"))
    admin.add_view(SecureModelView(OrderItem, db.session, category="Operations"))
    admin.add_view(SecureModelView(Payment, db.session, category="Operations"))
    admin.add_view(SecureModelView(Receipt, db.session, category="Operations"))
    admin.add_view(ContactMessageAdminView(ContactMessage, db.session, category="Communication"))
    admin.add_view(UserAdminView(User, db.session, category="Users"))

    return admin