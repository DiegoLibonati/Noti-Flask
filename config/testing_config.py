from config.default_config import BaseConfig


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    ENV = "testing"
    SECRET_KEY = "testing-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
