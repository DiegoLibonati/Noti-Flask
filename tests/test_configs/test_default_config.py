import pytest

from src.configs.default_config import DefaultConfig


class TestDefaultConfig:
    @pytest.mark.unit
    def test_debug_is_false(self) -> None:
        assert DefaultConfig.DEBUG is False

    @pytest.mark.unit
    def test_testing_is_false(self) -> None:
        assert DefaultConfig.TESTING is False

    @pytest.mark.unit
    def test_track_modifications_is_false(self) -> None:
        assert DefaultConfig.SQLALCHEMY_TRACK_MODIFICATIONS is False

    @pytest.mark.unit
    def test_secret_key_has_default(self) -> None:
        assert DefaultConfig.SECRET_KEY is not None
        assert len(DefaultConfig.SECRET_KEY) > 0

    @pytest.mark.unit
    def test_login_route_is_set(self) -> None:
        assert DefaultConfig.LOGIN_ROUTE is not None
        assert "login" in DefaultConfig.LOGIN_ROUTE

    @pytest.mark.unit
    def test_logout_route_is_set(self) -> None:
        assert DefaultConfig.LOGOUT_ROUTE is not None
        assert "logout" in DefaultConfig.LOGOUT_ROUTE

    @pytest.mark.unit
    def test_sign_up_route_is_set(self) -> None:
        assert DefaultConfig.SIGN_UP_ROUTE is not None
        assert "sign_up" in DefaultConfig.SIGN_UP_ROUTE

    @pytest.mark.unit
    def test_home_view_is_set(self) -> None:
        assert DefaultConfig.HOME_VIEW is not None
        assert "home" in DefaultConfig.HOME_VIEW

    @pytest.mark.unit
    def test_login_view_is_set(self) -> None:
        assert DefaultConfig.LOGIN_VIEW is not None
        assert "login" in DefaultConfig.LOGIN_VIEW

    @pytest.mark.unit
    def test_route_paths_start_with_slash(self) -> None:
        assert DefaultConfig.LOGIN_ROUTE_PATH.startswith("/")
        assert DefaultConfig.LOGOUT_ROUTE_PATH.startswith("/")
        assert DefaultConfig.SIGN_UP_ROUTE_PATH.startswith("/")

    @pytest.mark.unit
    def test_view_paths_start_with_slash(self) -> None:
        assert DefaultConfig.LOGIN_VIEW_PATH.startswith("/")
        assert DefaultConfig.SIGN_UP_VIEW_PATH.startswith("/")
        assert DefaultConfig.HOME_VIEW_PATH.startswith("/")

    @pytest.mark.unit
    def test_port_is_integer(self) -> None:
        assert isinstance(DefaultConfig.PORT, int)
