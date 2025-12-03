import secrets
from flask import request, jsonify
from functools import wraps
from backend.database.models import Account, Session
from backend.database import db
import bcrypt

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(to, subject, body):
    email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    port = int(os.getenv("EMAIL_PORT", 587))

    msg = MIMEMultipart()
    msg["From"] = email
    msg["To"] = to
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(email, password)
        server.send_message(msg)
        server.quit()
        print("Email sent!")
    except Exception as e:
        print("EMAIL ERROR:", e)


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

def get_account_from_header():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    parts = auth_header.split(" ")
    token = parts[1]
    session = Session.query.filter_by(token=token).first()

    if not session:
        return None

    account = Account.query.filter_by(account_id=session.account_id).first()
    return account


def require_account():
    account = get_account_from_request()
    if not account:
        return None, {"error": "Unauthorized"}, 401
    return account, None, None

def require_manager():
    account = get_account_from_header()
    if not account or account.role != "manager":
        return None, {"error": "Forbidden"}, 403
    return account, None, None

def hash_password(password):
    """
    Hashes a plain-text password using bcrypt.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')