from unittest.mock import patch

import pytest
from flask import Flask
from flask.testing import FlaskClient


class TestAuthViewLogin:
    @pytest.mark.unit
    def test_login_view_returns_200(self, client: FlaskClient) -> None:
        with patch("src.views.v1.auth_view.render_template", return_value="<html>login</html>"):
            response = client.get("/views/v1/auth/login")
        assert response.status_code == 200

    @pytest.mark.unit
    def test_login_view_content_type_is_html(self, client: FlaskClient) -> None:
        with patch("src.views.v1.auth_view.render_template", return_value="<html>login</html>"):
            response = client.get("/views/v1/auth/login")
        assert "text/html" in response.content_type

    @pytest.mark.unit
    def test_login_view_calls_render_template(self, client: FlaskClient) -> None:
        with patch("src.views.v1.auth_view.render_template", return_value="<html>x</html>") as mock_render:
            client.get("/views/v1/auth/login")
        mock_render.assert_called_once()

    @pytest.mark.unit
    def test_login_view_passes_context(self, client: FlaskClient) -> None:
        with patch("src.views.v1.auth_view.render_template", return_value="<html>x</html>") as mock_render:
            client.get("/views/v1/auth/login")
        call_kwargs: dict = mock_render.call_args.kwargs
        assert "context" in call_kwargs


class TestAuthViewSignUp:
    @pytest.mark.unit
    def test_sign_up_view_returns_200(self, client: FlaskClient) -> None:
        with patch("src.views.v1.auth_view.render_template", return_value="<html>signup</html>"):
            response = client.get("/views/v1/auth/sign_up")
        assert response.status_code == 200

    @pytest.mark.unit
    def test_sign_up_view_calls_render_template(self, client: FlaskClient) -> None:
        with patch("src.views.v1.auth_view.render_template", return_value="<html>x</html>") as mock_render:
            client.get("/views/v1/auth/sign_up")
        mock_render.assert_called_once()

    @pytest.mark.unit
    def test_sign_up_view_passes_context(self, client: FlaskClient) -> None:
        with patch("src.views.v1.auth_view.render_template", return_value="<html>x</html>") as mock_render:
            client.get("/views/v1/auth/sign_up")
        call_kwargs: dict = mock_render.call_args.kwargs
        assert "context" in call_kwargs


class TestAuthViewBeforeRequest:
    @pytest.mark.unit
    def test_before_request_skips_redirect_in_testing_mode(self, app: Flask, client: FlaskClient) -> None:
        assert app.config["TESTING"] is True
        with patch("src.views.v1.auth_view.render_template", return_value="<html>x</html>"):
            response = client.get("/views/v1/auth/login")
        assert response.status_code == 200
