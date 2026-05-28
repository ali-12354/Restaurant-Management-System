from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from models import User


def _identity_user():
    identity = get_jwt_identity()
    if not identity:
        return None
    return User.query.get(identity)


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = _identity_user()
        if not user or user.role != "admin":
            return jsonify({"message": "Admin access required"}), 403
        return fn(*args, **kwargs)

    return wrapper


def current_user_or_none():
    return _identity_user()