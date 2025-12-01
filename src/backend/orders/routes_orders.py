from flask import Blueprint, request, jsonify
from backend.database import db
from backend.database.models import Order, OrderItem, Book
from backend.utils import get_account_from_header

orders_bp = Blueprint("orders", __name__)


@orders_bp.post("/")
def create_order():
    account = get_account_from_header()
    if not account:
        return {"error": "Unauthorized"}, 401

    data = request.json
    if not data or "items" not in data:
        return {"error": "Missing items"}, 400

    items = data["items"]
    payment_status = data.get("payment_status", "paid")

    order = Order(
        account_id=account.account_id,
        total_cost=sum(item["price"] for item in items),
        payment_status=payment_status
    )
    db.session.add(order)
    db.session.commit()  # order_id is created here

    for item in items:
        order_item = OrderItem(
            order_id=order.order_id,
            book_id=item["book_id"],
            item_price=item["price"]
        )
        db.session.add(order_item)

    db.session.commit()

    return {"message": "Order created", "order_id": order.order_id}, 201


@orders_bp.get("/my_orders")
def my_orders():
    account = get_account_from_header()
    if not account:
        return {"error": "Unauthorized"}, 401

    orders = Order.query.filter_by(account_id=account.account_id).all()

    result = []
    for o in orders:
        result.append({
            "order_id": o.order_id,
            "total_cost": float(o.total_cost),
            "payment_status": o.payment_status,
            "created_at": o.created_at.isoformat(),
        })

    return jsonify(result)


@orders_bp.get("/<int:order_id>")
def get_order(order_id):
    account = get_account_from_header()
    if not account:
        return {"error": "Unauthorized"}, 401

    order = Order.query.get(order_id)
    if not order:
        return {"error": "Order not found"}, 404

    if order.account_id != account.account_id:
        return {"error": "Forbidden"}, 403

    items = OrderItem.query.filter_by(order_id=order_id).all()

    item_list = []
    for item in items:
        book = Book.query.get(item.book_id)
        item_list.append({
            "order_item_id": item.order_item_id,
            "book_id": item.book_id,
            "title": book.title if book else None,
            "price": float(item.item_price),
        })

    return jsonify({
        "order_id": order.order_id,
        "total_cost": float(order.total_cost),
        "payment_status": order.payment_status,
        "created_at": order.created_at.isoformat(),
        "items": item_list
    })
