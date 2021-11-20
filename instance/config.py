import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    #CSRF_ENABLED = True
    SECRET = os.urandom(16)


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': [DevelopmentConfig, 'test-assets/Images/'],
    'testing': [TestingConfig, 'test-assets/Images/'],
    'production': [ProductionConfig, 'Images/']
}
