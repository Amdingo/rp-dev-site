class BaseConfig:
    """Basic configuration for extension"""
    TESTING = False


class DevConfig(BaseConfig):
    """Development"""
    pass


class TestConfig(BaseConfig):
    """Testing"""
    TESTING = True


class ProdConfig(BaseConfig):
    """Production"""
    pass
