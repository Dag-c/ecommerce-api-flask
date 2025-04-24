import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

dotenv_loaded = load_dotenv()

# Create the directory if It doesn't exist
os.makedirs('logs', exist_ok=True)

# Config the log file
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=3)
file_handler.setLevel(logging.DEBUG)
formatter =logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)
file_handler.setFormatter(formatter)

#Set to global logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

class Config:
    print(dotenv_loaded)
    if dotenv_loaded:
        USER = os.getenv("POSTGRES_USER_DEVELOPMENT")
        PASSWORD = os.getenv("POSTGRES_PASSWORD_DEVELOPMENT")
        HOST = os.getenv("POSTGRES_HOST_DEVELOPMENT")
        DATABASE = os.getenv("POSTGRES_DB_DEVELOPMENT")
        REDIS_URL = os.getenv("REDIS_URL_DEVELOPMENT")
    else:
        USER = os.getenv("POSTGRES_USER_PRODUCTION")
        PASSWORD = os.getenv("POSTGRES_PASSWORD_PRODUCTION")
        HOST = os.getenv("POSTGRES_HOST_PRODUCTION")
        DATABASE = os.getenv("POSTGRES_DB_PRODUCTION")
        REDIS_URL = os.getenv("REDIS_URL_PRODUCTION")

    print(REDIS_URL)
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    SECRET_KEY = os.getenv("SECRET_KEY")

