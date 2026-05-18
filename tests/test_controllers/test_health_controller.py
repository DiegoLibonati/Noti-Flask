import pytest
from flask import Flask
from flask.testing import FlaskClient

from src.constants.codes import CODE_SUCCESS_HEALTH, CODE_SUCCESS_READY
from src.constants.messages import MESSAGE_SUCCESS_HEALTH, MESSAGE_SUCCESS_READY
from src.controllers.health_controller import health, ready


class TestHealthControllerHealth:
    @pytest.mark.unit
    def test_health_route_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/health/")
        assert response.status_code == 200

    @pytest.mark.unit
    def test_health_route_returns_expected_json(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/health/")
        data: dict = response.get_json()
        assert data["code"] == CODE_SUCCESS_HEALTH
        assert data["message"] == MESSAGE_SUCCESS_HEALTH

    @pytest.mark.unit
    def test_health_callable_returns_200_in_app_context(self, app: Flask) -> None:
        with app.app_context():
            response, status = health()
        assert status == 200
        assert response.get_json()["code"] == CODE_SUCCESS_HEALTH


class TestHealthControllerReady:
    @pytest.mark.unit
    def test_ready_callable_returns_200(self, app: Flask) -> None:
        with app.app_context():
            response, status = ready()
        assert status == 200

    @pytest.mark.unit
    def test_ready_callable_returns_expected_json(self, app: Flask) -> None:
        with app.app_context():
            response, _ = ready()
        data: dict = response.get_json()
        assert data["code"] == CODE_SUCCESS_READY
        assert data["message"] == MESSAGE_SUCCESS_READY
