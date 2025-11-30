from flask import Blueprint, request, jsonify
from backend.database.models import Account, Session
from backend.database.db import db
from backend.auth.utils import verify_password, generate_token, require_auth

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    account = Account.query.filter_by(username=username).first()

    if not account or not verify_password(password, account.hashed_password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token()

    session = Session(
        account_id=account.account_id,
        token=token
    )
    db.session.add(session)
    db.session.commit()

    return jsonify({
        "message": "Login successful",
        "token": token,
        "role": account.role,
    })

@auth_bp.post("/logout")
@require_auth
def logout(account):
    # get token from header
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ")[1]

    # remove session entry
    Session.query.filter_by(token=token).delete()
    db.session.commit()

    return jsonify({"message": "Logged out successfully"})
