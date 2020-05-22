import os 

class Config(object):
    """Parent Configuration Class"""
    DEBUG = False
    CSRF_ENABLED = True
    SQLALCHEMY_ECHO = False
    ENVIRONMENT = 'Development'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_ENGINE_OPTIONS = os.getenv('SQLALCHEMY_ENGINE_OPTIONS')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True  # enable blacklist feature
    JWT_BLACKLIST_TOKEN_CHECKS = os.getenv('JWT_BLACKLIST_TOKEN_CHECKS')
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAIL_SERVER = os.getenv('MAIL_SERVER'),
    MAIL_PORT = os.getenv('JWT_SECRET_KEY'),
    MAIL_USE_TLS = os.getenv('MAIL_PORT'),
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL'),
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_ASCII_ATTACHMENTS = os.getenv('MAIL_ASCII_ATTACHMENTS')

class Development(Config):
    """Configurations for Development."""
    DEBUG = True
    ENVIRONMENT = 'Development'
    

class Testing (Config):
    """Configurations for Testing, with a separate test database."""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    ENVIRONMENT = 'Development'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

class Production(Config):
    """Configurations for Production."""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    ENVIRONMENT = 'Production'
    TESTING = False
