import logging
from flask import jsonify
from flask_limiter.errors import RateLimitExceeded
from sqlalchemy.exc import SQLAlchemyError
from app.utils.exceptions import *


class ErrorHandler:
    @staticmethod
    def init_app(app):
        """
        """
        @app.errorhandler(BadRequestsError)
        def handle_bad_request_error(error):
            logging.warning("Bad Request", exc_info=True)
            return jsonify({"error": "Bad Request", "message": error.message}), 400

        @app.errorhandler(InvalidTokenFormat)
        def handle_invalid_token_format(error):
            logging.warning("Invalid token format", exc_info=True)
            return jsonify({"error": "Invalid Token Format", "message": error.message}), 400

        @app.errorhandler(TokenMissing)
        def handle_token_missing(error):
            logging.warning("Token missing", exc_info=True)
            return jsonify({"error": "Token Missing", "message": error.message}), 401

        @app.errorhandler(TokenExpired)
        def handle_token_expired(error):
            logging.info("Token expired", exc_info=True)
            return jsonify({"error": "Token Expired", "message": error.message}), 401

        @app.errorhandler(TokenInvalid)
        def handle_token_invalid(error):
            logging.warning("Invalid token", exc_info=True)
            return jsonify({"error": "Invalid Token", "message": error.message}), 401

        @app.errorhandler(ResourceNotFound)
        def handle_resource_not_found(error):
            logging.info("Resource not found", exc_info=True)
            return jsonify({"error": "Resource Not Found", "message": error.message}), 404

        @app.errorhandler(RateLimitExceeded)
        def handle_rate_limit_exceeded(error):
            logging.warning("Too Many Requests", exc_info=True)
            return jsonify({
                "error": "Too Many Requests",
                "message": str(error)
            }), 429

        @app.errorhandler(SQLAlchemyError)
        def handle_sqlalchemy_error(error):
            logging.error("Database error", exc_info=True)
            return jsonify({
                "error": "Database Error",
                "message": "An error occurred while interacting with the database"
            }), 500

        @app.errorhandler(Exception)
        def handle_unexpected_error(error):
            logging.critical("Internal Server Error", exc_info=True)
            return jsonify({
                "error": "Internal Server Error",
                "message": "An unexpected error occurred"
            }), 500
