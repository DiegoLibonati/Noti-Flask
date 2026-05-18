import pytest

from src.constants import vars as project_vars


class TestFolderNames:
    @pytest.mark.unit
    def test_static_folder_name(self) -> None:
        assert project_vars.STATIC_FOLDER_NAME == "static"

    @pytest.mark.unit
    def test_css_folder_name(self) -> None:
        assert project_vars.CSS_FOLDER_NAME == "css"

    @pytest.mark.unit
    def test_scss_folder_name(self) -> None:
        assert project_vars.SCSS_FOLDER_NAME == "scss"

    @pytest.mark.unit
    def test_js_folder_name(self) -> None:
        assert project_vars.JS_FOLDER_NAME == "js"

    @pytest.mark.unit
    def test_ts_folder_name(self) -> None:
        assert project_vars.TS_FOLDER_NAME == "ts"

    @pytest.mark.unit
    def test_general_templates_folder_name(self) -> None:
        assert project_vars.GENERAL_TEMPLATES_FOLDER_NAME == "templates"

    @pytest.mark.unit
    def test_auth_templates_folder_name(self) -> None:
        assert project_vars.AUTH_TEMPLATES_FOLDER_NAME == "auth"

    @pytest.mark.unit
    def test_app_templates_folder_name(self) -> None:
        assert project_vars.APP_TEMPLATES_FOLDER_NAME == "app"


class TestVersions:
    @pytest.mark.unit
    def test_version_views_is_string(self) -> None:
        assert isinstance(project_vars.VERSION_VIEWS, str)
        assert len(project_vars.VERSION_VIEWS) > 0

    @pytest.mark.unit
    def test_version_blueprints_is_string(self) -> None:
        assert isinstance(project_vars.VERSION_BLUEPRINTS, str)
        assert len(project_vars.VERSION_BLUEPRINTS) > 0


class TestRouteNames:
    @pytest.mark.unit
    def test_auth_blueprint_route_name(self) -> None:
        assert project_vars.AUTH_BLUEPRINT_ROUTE_NAME == "auth"

    @pytest.mark.unit
    def test_notes_blueprint_route_name(self) -> None:
        assert project_vars.NOTES_BLUEPRINT_ROUTE_NAME == "notes"

    @pytest.mark.unit
    def test_auth_view_route_name(self) -> None:
        assert project_vars.AUTH_VIEW_ROUTE_NAME == "auth_view"

    @pytest.mark.unit
    def test_app_view_route_name(self) -> None:
        assert project_vars.APP_VIEW_ROUTE_NAME == "app_view"


class TestBlueprintPaths:
    @pytest.mark.unit
    def test_prefix_blueprints_path_starts_with_api(self) -> None:
        assert project_vars.PREFIX_BLUEPRINTS_PATH.startswith("/api/")

    @pytest.mark.unit
    def test_prefix_blueprints_path_contains_version(self) -> None:
        assert project_vars.VERSION_BLUEPRINTS in project_vars.PREFIX_BLUEPRINTS_PATH

    @pytest.mark.unit
    def test_blueprint_auth_path_uses_prefix(self) -> None:
        assert project_vars.BLUEPRINT_AUTH_PATH.startswith(project_vars.PREFIX_BLUEPRINTS_PATH)
        assert project_vars.BLUEPRINT_AUTH_PATH.endswith("/auth")

    @pytest.mark.unit
    def test_blueprint_notes_path_uses_prefix(self) -> None:
        assert project_vars.BLUEPRINT_NOTES_PATH.startswith(project_vars.PREFIX_BLUEPRINTS_PATH)
        assert project_vars.BLUEPRINT_NOTES_PATH.endswith("/notes")

    @pytest.mark.unit
    def test_blueprint_health_path_uses_prefix(self) -> None:
        assert project_vars.BLUEPRINT_HEALTH_PATH.startswith(project_vars.PREFIX_BLUEPRINTS_PATH)
        assert project_vars.BLUEPRINT_HEALTH_PATH.endswith("/health")


class TestViewPaths:
    @pytest.mark.unit
    def test_prefix_views_path_starts_with_views(self) -> None:
        assert project_vars.PREFIX_VIEWS_PATH.startswith("/views/")

    @pytest.mark.unit
    def test_prefix_views_path_contains_version(self) -> None:
        assert project_vars.VERSION_VIEWS in project_vars.PREFIX_VIEWS_PATH

    @pytest.mark.unit
    def test_view_auth_path_uses_prefix(self) -> None:
        assert project_vars.VIEW_AUTH_PATH.startswith(project_vars.PREFIX_VIEWS_PATH)
        assert project_vars.VIEW_AUTH_PATH.endswith("/auth")

    @pytest.mark.unit
    def test_view_app_path_uses_prefix(self) -> None:
        assert project_vars.VIEW_APP_PATH.startswith(project_vars.PREFIX_VIEWS_PATH)
        assert project_vars.VIEW_APP_PATH.endswith("/app")


class TestTemplateNames:
    @pytest.mark.unit
    def test_template_login_name(self) -> None:
        assert project_vars.TEMPLATE_LOGIN_NAME == "login.html"

    @pytest.mark.unit
    def test_template_sign_up_name(self) -> None:
        assert project_vars.TEMPLATE_SIGN_UP_NAME == "sign_up.html"

    @pytest.mark.unit
    def test_template_home_name(self) -> None:
        assert project_vars.TEMPLATE_HOME_NAME == "home.html"

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "name",
        [
            "TEMPLATE_LOGIN_NAME",
            "TEMPLATE_SIGN_UP_NAME",
            "TEMPLATE_HOME_NAME",
        ],
    )
    def test_template_name_ends_with_html(self, name: str) -> None:
        assert getattr(project_vars, name).endswith(".html")
