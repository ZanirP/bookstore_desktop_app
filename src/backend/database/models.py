from backend.database import db
from datetime import datetime


book_genres = db.Table(
    "book_genres",
    db.Column("book_id", db.Integer, db.ForeignKey("books.book_id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.genre_id"), primary_key=True),
)


class Account(db.Model):
    __tablename__ = "accounts"

    account_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    role = db.Column(db.String(50), nullable=False)

    orders = db.relationship("Order", back_populates="account", cascade="all,delete")
    reviews = db.relationship("Review", back_populates="account", cascade="all,delete")
    notifications = db.relationship("Notification", back_populates="account", cascade="all,delete")
    sessions = db.relationship("Session", back_populates="account", cascade="all,delete")

    def __repr__(self):
        return f"<Account {self.username}>"


class Session(db.Model):
    __tablename__ = "sessions"

    session_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    account = db.relationship("Account", back_populates="sessions")

    def __repr__(self):
        return f"<Session {self.session_id}>"


class Book(db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    synopsis = db.Column(db.Text, nullable=False)
    price_buy = db.Column(db.Numeric(10, 2), nullable=False)
    price_rent = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.now)

    reviews = db.relationship("Review", back_populates="book", cascade="all,delete")
    order_items = db.relationship("OrderItem", back_populates="book", cascade="all,delete")

    genres = db.relationship("Genre", secondary=book_genres, back_populates="books")

    def __repr__(self):
        return f"<Book {self.title}>"


class Genre(db.Model):
    __tablename__ = "genres"

    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    books = db.relationship("Book", secondary=book_genres, back_populates="genres")

    def __repr__(self):
        return f"<Genre {self.name}>"


class Order(db.Model):
    __tablename__ = "orders"

    order_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"), nullable=False)
    total_cost = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    account = db.relationship("Account", back_populates="orders")
    order_items = db.relationship("OrderItem", back_populates="order", cascade="all,delete")

    def __repr__(self):
        return f"<Order {self.order_id}>"


class OrderItem(db.Model):
    __tablename__ = "order_items"

    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    item_price = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship("Order", back_populates="order_items")
    book = db.relationship("Book", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem {self.order_item_id}>"


class Notification(db.Model):
    __tablename__ = "notifications"

    notification_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    account = db.relationship("Account", back_populates="notifications")

    def __repr__(self):
        return f"<Notification {self.notification_id}>"


class Review(db.Model):
    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    review_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    account = db.relationship("Account", back_populates="reviews")
    book = db.relationship("Book", back_populates="reviews")

    def __repr__(self):
        return f"<Review {self.review_id}>"
