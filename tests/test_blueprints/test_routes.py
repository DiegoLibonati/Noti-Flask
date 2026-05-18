import pytest
from flask import Flask


class TestBlueprintsRegistration:
    @pytest.mark.unit
    def test_health_blueprint_is_registered(self, app: Flask) -> None:
        registered: list[str] = list(app.blueprints)
        assert "health" in registered

    @pytest.mark.unit
    def test_notes_blueprint_is_registered(self, app: Flask) -> None:
        registered: list[str] = list(app.blueprints)
        assert "notes" in registered

    @pytest.mark.unit
    def test_auth_blueprint_is_registered(self, app: Flask) -> None:
        registered: list[str] = list(app.blueprints)
        assert "auth" in registered

    @pytest.mark.unit
    def test_app_view_blueprint_is_registered(self, app: Flask) -> None:
        registered: list[str] = list(app.blueprints)
        assert "app_view" in registered

    @pytest.mark.unit
    def test_auth_view_blueprint_is_registered(self, app: Flask) -> None:
        registered: list[str] = list(app.blueprints)
        assert "auth_view" in registered


class TestHealthBlueprintRoutes:
    @pytest.mark.unit
    def test_health_root_route_exists(self, app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in app.url_map.iter_rules()]
        assert "/api/v1/health/" in rules

    @pytest.mark.unit
    def test_health_endpoint_uses_health_prefix(self, app: Flask) -> None:
        endpoints: list[str] = [rule.endpoint for rule in app.url_map.iter_rules()]
        health_endpoints: list[str] = [e for e in endpoints if e.startswith("health.")]
        assert len(health_endpoints) > 0


class TestNoteBlueprintRoutes:
    @pytest.mark.unit
    def test_notes_alive_route_exists(self, app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in app.url_map.iter_rules()]
        assert "/api/v1/notes/alive" in rules

    @pytest.mark.unit
    def test_notes_get_all_route_exists(self, app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in app.url_map.iter_rules()]
        assert "/api/v1/notes/" in rules

    @pytest.mark.unit
    def test_notes_delete_route_exists(self, app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in app.url_map.iter_rules()]
        assert "/api/v1/notes/<id>" in rules

    @pytest.mark.unit
    def test_notes_endpoints_use_notes_prefix(self, app: Flask) -> None:
        endpoints: list[str] = [rule.endpoint for rule in app.url_map.iter_rules()]
        note_endpoints: list[str] = [e for e in endpoints if e.startswith("notes.")]
        assert len(note_endpoints) > 0


class TestAuthBlueprintRoutes:
    @pytest.mark.unit
    def test_auth_alive_route_exists(self, app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in app.url_map.iter_rules()]
        assert "/api/v1/auth/alive" in rules

    @pytest.mark.unit
    def test_auth_login_route_exists(self, app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in app.url_map.iter_rules()]
        assert "/api/v1/auth/login" in rules

    @pytest.mark.unit
    def test_auth_logout_route_exists(self, app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in app.url_map.iter_rules()]
        assert "/api/v1/auth/logout" in rules

    @pytest.mark.unit
    def test_auth_sign_up_route_exists(self, app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in app.url_map.iter_rules()]
        assert "/api/v1/auth/sign_up" in rules


class TestViewRoutes:
    @pytest.mark.unit
    def test_home_view_route_exists(self, app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in app.url_map.iter_rules()]
        assert "/views/v1/app/home" in rules

    @pytest.mark.unit
    def test_auth_view_login_route_exists(self, app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in app.url_map.iter_rules()]
        assert "/views/v1/auth/login" in rules

    @pytest.mark.unit
    def test_auth_view_sign_up_route_exists(self, app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in app.url_map.iter_rules()]
        assert "/views/v1/auth/sign_up" in rules
