import os


class BaseConfig:
    """Basic configuration for extension"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    """Development"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestConfig(BaseConfig):
    """Testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')


class ProdConfig(BaseConfig):
    """Production"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
