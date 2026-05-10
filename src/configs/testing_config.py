from src.configs.default_config import DefaultConfig


class TestingConfig(DefaultConfig):
    TESTING = True
    DEBUG = True
    ENV = "testing"
    SECRET_KEY = "testing-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
