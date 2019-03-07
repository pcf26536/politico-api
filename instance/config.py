"""Configuration file"""
import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    SECRET = os.getenv('SECRET')
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SENDGRID_DEFAULT_FROM = os.getenv('SENDGRID_DEFAULT_FROM')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_URL')


class TestingConfig(Config):
    """Configurations for Testing"""
    TESTING = True
    DEBUG = True
    DATABASE_URL = os.getenv('TEST_DATABASE_URL')


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    DATABASE_URL = os.getenv('DATABASE_URL')


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
