import os

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'PASSWORD'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///grounds.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Other Configuration
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
