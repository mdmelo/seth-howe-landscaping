import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SESSION_SECRET') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@sethhowelandscaping.com')
    
    # Contact configuration
    CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', 'seth@sethhowelandscaping.com')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@sethhowelandscaping.com')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        SQLALCHEMY_DATABASE_URI = database_url
        if database_url.startswith('postgres://'):
            SQLALCHEMY_DATABASE_URI = database_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_recycle": 300,
            "pool_pre_ping": True,
        }
    else:
        # Fallback to SQLite for development
        SQLALCHEMY_DATABASE_URI = 'sqlite:///landscaping.db'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required for production")
    
    SQLALCHEMY_DATABASE_URI = database_url
    if database_url.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = database_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 20,
    }

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}