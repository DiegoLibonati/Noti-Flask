from typing import Any

import pytest
from flask import Flask

from src.utils.helpers import get_context_by_key, get_extra_files, get_watch_patterns


class TestGetContextByKey:
    @pytest.mark.unit
    def test_login_context_has_sign_up_view(self, app: Flask) -> None:
        with app.app_context():
            result: dict[str, Any] = get_context_by_key(app=app, key="login")
        assert "sign_up_view" in result

    @pytest.mark.unit
    def test_login_context_has_login_route(self, app: Flask) -> None:
        with app.app_context():
            result: dict[str, Any] = get_context_by_key(app=app, key="login")
        assert "login_route" in result

    @pytest.mark.unit
    def test_register_context_has_login_view(self, app: Flask) -> None:
        with app.app_context():
            result: dict[str, Any] = get_context_by_key(app=app, key="register")
        assert "login_view" in result

    @pytest.mark.unit
    def test_register_context_has_sign_up_route(self, app: Flask) -> None:
        with app.app_context():
            result: dict[str, Any] = get_context_by_key(app=app, key="register")
        assert "sign_up_route" in result

    @pytest.mark.unit
    def test_home_context_has_logout_route(self, app: Flask) -> None:
        with app.app_context():
            result: dict[str, Any] = get_context_by_key(app=app, key="home")
        assert "logout_route" in result

    @pytest.mark.unit
    def test_home_context_has_current_route(self, app: Flask) -> None:
        with app.app_context():
            result: dict[str, Any] = get_context_by_key(app=app, key="home")
        assert result["current_route"] == "Home"

    @pytest.mark.unit
    def test_unknown_key_returns_empty_dict(self, app: Flask) -> None:
        with app.app_context():
            result: dict[str, Any] = get_context_by_key(app=app, key="unknown_key")
        assert result == {}

    @pytest.mark.unit
    def test_extra_kwargs_are_merged_into_result(self, app: Flask) -> None:
        with app.app_context():
            result: dict[str, Any] = get_context_by_key(app=app, key="home", extra_key="extra_val")
        assert result["extra_key"] == "extra_val"

    @pytest.mark.unit
    def test_extra_kwargs_override_base_context(self, app: Flask) -> None:
        with app.app_context():
            result: dict[str, Any] = get_context_by_key(app=app, key="home", current_route="Override")
        assert result["current_route"] == "Override"


class TestGetWatchPatterns:
    @pytest.mark.unit
    def test_returns_non_empty_list(self) -> None:
        result: list[str] = get_watch_patterns()
        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.unit
    def test_all_entries_are_strings(self) -> None:
        result: list[str] = get_watch_patterns()
        assert all(isinstance(p, str) for p in result)


class TestGetExtraFiles:
    @pytest.mark.unit
    def test_returns_list(self) -> None:
        result: list[str] = get_extra_files()
        assert isinstance(result, list)

    @pytest.mark.unit
    def test_all_entries_are_strings(self) -> None:
        result: list[str] = get_extra_files()
        assert all(isinstance(f, str) for f in result)
