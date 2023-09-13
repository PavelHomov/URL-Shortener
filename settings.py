from dotenv import load_dotenv
import os

load_dotenv()


class Config(object):
    """
    Класс конфига.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        default='sqlite:///db.sqlite3',
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv(
        'SECRET_KEY',
        default='YOUR_SECRET_KEY',
    )
