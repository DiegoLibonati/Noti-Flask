import pytest

from src.configs.testing_config import TestingConfig


class TestTestingConfig:
    @pytest.mark.unit
    def test_testing_flag_is_true(self) -> None:
        assert TestingConfig.TESTING is True

    @pytest.mark.unit
    def test_debug_is_true(self) -> None:
        assert TestingConfig.DEBUG is True

    @pytest.mark.unit
    def test_env_is_testing(self) -> None:
        assert TestingConfig.ENV == "testing"

    @pytest.mark.unit
    def test_secret_key_is_set(self) -> None:
        assert TestingConfig.SECRET_KEY is not None
        assert len(TestingConfig.SECRET_KEY) > 0

    @pytest.mark.unit
    def test_database_uri_uses_sqlite_memory(self) -> None:
        assert "sqlite" in TestingConfig.SQLALCHEMY_DATABASE_URI
        assert ":memory:" in TestingConfig.SQLALCHEMY_DATABASE_URI

    @pytest.mark.unit
    def test_track_modifications_is_false(self) -> None:
        assert TestingConfig.SQLALCHEMY_TRACK_MODIFICATIONS is False

    @pytest.mark.unit
    def test_check_connections_is_false(self) -> None:
        assert TestingConfig.CHECK_CONNECTIONS is False
