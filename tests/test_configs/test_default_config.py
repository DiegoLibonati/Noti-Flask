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

    @pytest.mark.unit
    def test_tz_has_default(self) -> None:
        assert DefaultConfig.TZ is not None
        assert isinstance(DefaultConfig.TZ, str)

    @pytest.mark.unit
    def test_max_content_length_is_integer(self) -> None:
        assert isinstance(DefaultConfig.MAX_CONTENT_LENGTH, int)
        assert DefaultConfig.MAX_CONTENT_LENGTH > 0

    @pytest.mark.unit
    def test_mysql_attributes_are_exposed(self) -> None:
        assert hasattr(DefaultConfig, "MYSQL_HOST")
        assert hasattr(DefaultConfig, "MYSQL_USER")
        assert hasattr(DefaultConfig, "MYSQL_PASSWORD")
        assert hasattr(DefaultConfig, "MYSQL_PORT")
        assert hasattr(DefaultConfig, "MYSQL_DB_NAME")

    @pytest.mark.unit
    def test_sqlalchemy_uri_uses_mysql_driver(self) -> None:
        assert DefaultConfig.SQLALCHEMY_DATABASE_URI.startswith("mysql+pymysql://")

    @pytest.mark.unit
    def test_sqlalchemy_uri_includes_mysql_components(self) -> None:
        uri: str = DefaultConfig.SQLALCHEMY_DATABASE_URI
        assert str(DefaultConfig.MYSQL_HOST) in uri
        assert str(DefaultConfig.MYSQL_USER) in uri
        assert str(DefaultConfig.MYSQL_PASSWORD) in uri
        assert str(DefaultConfig.MYSQL_PORT) in uri
        assert str(DefaultConfig.MYSQL_DB_NAME) in uri

    @pytest.mark.unit
    def test_route_constants_use_blueprint_names(self) -> None:
        assert DefaultConfig.GET_ALL_NOTES_ROUTE.startswith("notes.")
        assert DefaultConfig.CREATE_NOTE_ROUTE.startswith("notes.")
        assert DefaultConfig.DELETE_NOTE_ROUTE.startswith("notes.")
        assert DefaultConfig.EDIT_NOTE_ROUTE.startswith("notes.")

    @pytest.mark.unit
    def test_note_route_paths_use_notes_prefix(self) -> None:
        assert "/notes" in DefaultConfig.GET_ALL_NOTES_ROUTE_PATH
        assert "/notes" in DefaultConfig.CREATE_NOTE_ROUTE_PATH
        assert "/notes" in DefaultConfig.DELETE_NOTE_ROUTE_PATH
        assert "/notes" in DefaultConfig.EDIT_NOTE_ROUTE_PATH
