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

    total_cost = 0
    order_items_to_create = []

    for item in items:
        book_id = item.get("book_id")
        action = item.get("action", "buy")

        book = Book.query.get(book_id)
        if not book:
            return {"error": f"Book {book_id} not found"}, 404

        price = book.price_rent if action == "rent" else book.price_buy
        total_cost += price

        order_items_to_create.append({
            "book_id": book_id,
            "price": price
        })

    order = Order(
        account_id=account.account_id,
        total_cost=total_cost,
        payment_status="unpaid"
    )
    db.session.add(order)
    db.session.commit()

    for oi in order_items_to_create:
        order_item = OrderItem(
            order_id=order.order_id,
            book_id=oi["book_id"],
            item_price=oi["price"]
        )
        db.session.add(order_item)

    db.session.commit()

    return {
        "message": "Order created",
        "order_id": order.order_id
    }, 201



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
