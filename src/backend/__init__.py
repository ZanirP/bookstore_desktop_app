from flask import Flask
from backend.config import Config
from backend.database import db, migrate



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from backend.auth.routes_auth import auth_bp
    from backend.database import models

    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app