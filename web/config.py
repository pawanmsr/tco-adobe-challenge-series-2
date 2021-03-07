from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    FLASK_APP = 'wsgi.py'
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')
    BASE_URL = environ.get('BASE_URL')

    DEBUG = False
    TESTING = True

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Storage
    STORAGE_PATH = environ.get("STORAGE_PATH")

    # EMBED API
    EMBED_API_ID = environ.get("EMBED_API_ID")

    # NODE API
    MERGE = environ.get('MERGE')
    REORDER = environ.get('REORDER')
    SPLIT = environ.get('SPLIT')
    DELETE = environ.get('DELETE')
    SIGN = environ.get('SIGN')
