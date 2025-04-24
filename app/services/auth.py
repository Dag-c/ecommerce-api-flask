import bcrypt
import jwt
from functools import wraps
from flask import request
from datetime import datetime, timedelta, timezone
from app.models import User
from app.config import Config
from app.utils.exceptions import InvalidTokenFormat, TokenMissing, TokenExpired, TokenInvalid


def encrypt_password(password: str) -> str:
    # Create a salt and encrypt the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def check_password(user: User, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))


def generate_jwt_token(user: User) -> str:
    exp_time = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {
        'sub': str(user.id),
        'email': str(user.email),
        'exp': int(exp_time.timestamp())
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        # Verify if token is in header
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except IndexError as e:
                raise InvalidTokenFormat()
        if not token:
            raise TokenMissing()

        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise TokenExpired()
        except jwt.InvalidTokenError:
            raise TokenInvalid()

        return f(*args, **kwargs)
    return decorator
