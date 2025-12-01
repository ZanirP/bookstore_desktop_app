from flask import Flask
from backend.config import Config
from backend.database import db, migrate



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from backend.database import models

    from backend.auth.routes_auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from backend.books.routes_books import books_bp
    app.register_blueprint(books_bp, url_prefix='/books')

    from backend.orders.routes_orders import orders_bp
    app.register_blueprint(orders_bp, url_prefix="/orders")

    return app