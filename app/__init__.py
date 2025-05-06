from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
from flasgger import Swagger

from .config import Config
from .database import db
from .routes.users import users_bp
from .routes.products import products_bp
from .routes.orders import orders_bp
from .routes.auth import auth_bp
from .routes.email import email_bp
from .utils.error_handler import ErrorHandler


def create_app(config: Config = None):
    app = Flask(__name__)
    if config:
        app.config.from_object(config)
    else:
        app.config.from_object(Config)

    CORS(app, methods=["GET", "POST", "PATCH", "DELETE"],
         allow_headers=["Content-Type"])

    db.init_app(app)

    redis_connection = redis.Redis.from_url(app.config["REDIS_URL"])

    limiter = Limiter(
        get_remote_address,
        storage_uri=Config.REDIS_URL,
        app=app,
        default_limits=["100/hour"]
    )

    # Register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(email_bp)

    # Swagger
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Ecommerce API",
            "description": "This is the API documentation for my ecommerce project using Flask.",
            "version": "1.0.0",
            "termsOfService": "https://dag-c.github.io/diegodev-portfolio/#home",
            "contact": {
                "name": "Diego Armando Guillen de la Cruz",
                "email": "diego.guillen.d.cruz@gmail.com",
                "url": "https://dag-c.github.io/diegodev-portfolio/#home"
            },
            "license": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT"
            }
        },
        "schemes": ["http", "https"]
    }

    Swagger(app, template=swagger_template)

    ErrorHandler.init_app(app)

    with app.app_context():
        try:
            db.create_all()
        except SQLAlchemyError as db_error:
            print(f"Database error: {str(db_error)}")

    return app
