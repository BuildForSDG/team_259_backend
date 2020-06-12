import os 

class Config(object):
    """Parent Configuration Class"""
    DEBUG = False
    CSRF_ENABLED = True
    SQLALCHEMY_ECHO = False
    ENVIRONMENT = 'Development'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle': 280, 'pool_timeout': 100, 'pool_pre_ping': True}
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True  # enable blacklist feature
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USE_TLS = bool(os.getenv('MAIL_USE_TLS'))
    MAIL_USE_SSL = bool(os.getenv('MAIL_USE_SSL'))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_ASCII_ATTACHMENTS = bool(os.getenv('MAIL_ASCII_ATTACHMENTS'))
    
class Development(Config):
    """Configurations for Development."""
    DEBUG = True
    ENVIRONMENT = 'Development'
    

class Testing (Config):
    """Configurations for Testing, with a separate test database."""
    DEBUG = False
    ENVIRONMENT = 'Development'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ''

class Production(Config):
    """Configurations for Production."""
    DEBUG = False
    ENVIRONMENT = 'Production'
    TESTING = False
