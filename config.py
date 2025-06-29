import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SESSION_SECRET') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email configuration with defaults
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@sethhowelandscaping.com'
    
    # Contact configuration with defaults
    CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL') or 'seth@sethhowelandscaping.com'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@sethhowelandscaping.com'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
    # Default to SQLite if no DATABASE_URL is provided
    database_url = os.environ.get('DATABASE_URL') or 'sqlite:///landscaping.db'
    
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = database_url
    
    # Engine options for PostgreSQL
    if database_url.startswith('postgresql://'):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_recycle": 300,
            "pool_pre_ping": True,
        }

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
    # Default to SQLite if no DATABASE_URL is provided (for easy deployment)
    database_url = os.environ.get('DATABASE_URL') or 'sqlite:///landscaping.db'
    
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = database_url
    
    # Engine options for PostgreSQL
    if database_url.startswith('postgresql://'):
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