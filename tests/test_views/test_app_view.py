from unittest.mock import patch

import pytest
from flask import Flask
from flask.testing import FlaskClient


class TestAppViewHome:
    @pytest.mark.unit
    def test_home_redirects_when_not_authenticated(self, client: FlaskClient) -> None:
        response = client.get("/views/v1/app/home")
        assert response.status_code == 302

    @pytest.mark.integration
    def test_home_returns_200_when_authenticated(self, app: Flask, auth_client: FlaskClient, db_session: None) -> None:
        with patch("src.views.v1.app_view.render_template", return_value="<html>home</html>"):
            response = auth_client.get("/views/v1/app/home")
        assert response.status_code == 200

    @pytest.mark.integration
    def test_home_content_type_is_html_when_authenticated(self, app: Flask, auth_client: FlaskClient, db_session: None) -> None:
        with patch("src.views.v1.app_view.render_template", return_value="<html>home</html>"):
            response = auth_client.get("/views/v1/app/home")
        assert "text/html" in response.content_type

    @pytest.mark.integration
    def test_home_calls_render_template_when_authenticated(self, app: Flask, auth_client: FlaskClient, db_session: None) -> None:
        with patch("src.views.v1.app_view.render_template", return_value="<html>home</html>") as mock_render:
            auth_client.get("/views/v1/app/home")
        mock_render.assert_called_once()

    @pytest.mark.integration
    def test_home_passes_context_with_notes(self, app: Flask, auth_client: FlaskClient, db_session: None) -> None:
        with patch("src.views.v1.app_view.render_template", return_value="<html>home</html>") as mock_render:
            auth_client.get("/views/v1/app/home")
        call_kwargs: dict = mock_render.call_args.kwargs
        assert "context" in call_kwargs
        assert "notes" in call_kwargs["context"]
