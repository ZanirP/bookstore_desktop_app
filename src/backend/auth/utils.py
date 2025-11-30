import secrets
from flask import request, jsonify
from functools import wraps
from backend.database.models import Account, Session
from backend.database.db import db
import bcrypt

def generate_token():
    return secrets.token_hex(32)


def verify_password(plain_pw, hashed_pw):
    return bcrypt.checkpw(plain_pw.encode("utf-8"), hashed_pw.encode("utf-8"))


def get_account_from_request():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]

    session = Session.query.filter_by(token=token).first()
    if not session:
        return None

    return session.account  # thanks to SQLAlchemy relationship


def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        account = get_account_from_request()
        if not account:
            return jsonify({"error": "Unauthorized"}), 401

        return f(account, *args, **kwargs)  # pass user into function

    return wrapper


def require_role(role):
    def decorator(f):
        @wraps(f)
        def wrapper(account, *args, **kwargs):
            if account.role != role:
                return jsonify({"error": "Forbidden"}), 403
            return f(account, *args, **kwargs)

        return wrapper

    return decorator
