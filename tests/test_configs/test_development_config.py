import pytest

from src.configs.default_config import DefaultConfig
from src.configs.development_config import DevelopmentConfig


class TestDevelopmentConfig:
    @pytest.mark.unit
    def test_debug_is_true(self) -> None:
        assert DevelopmentConfig.DEBUG is True

    @pytest.mark.unit
    def test_env_is_development(self) -> None:
        assert DevelopmentConfig.ENV == "development"

    @pytest.mark.unit
    def test_testing_is_false(self) -> None:
        assert DevelopmentConfig.TESTING is False

    @pytest.mark.unit
    def test_inherits_from_default_config(self) -> None:
        assert issubclass(DevelopmentConfig, DefaultConfig)

    @pytest.mark.unit
    def test_inherits_track_modifications_false(self) -> None:
        assert DevelopmentConfig.SQLALCHEMY_TRACK_MODIFICATIONS is False
