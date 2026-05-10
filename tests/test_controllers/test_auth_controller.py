from unittest.mock import MagicMock, patch

import pytest
from flask import Flask
from flask.testing import FlaskClient

from src.services.encrypt_service import EncryptService


class TestAuthControllerAlive:
    @pytest.mark.unit
    def test_alive_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/auth/alive")
        assert response.status_code == 200

    @pytest.mark.unit
    def test_alive_returns_expected_json(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/auth/alive")
        data: dict = response.get_json()
        assert data["message"] == "I am Alive!"
        assert data["name_bp"] == "Auth"


class TestAuthControllerLogin:
    @pytest.mark.unit
    def test_login_returns_400_when_fields_missing(self, client: FlaskClient) -> None:
        response = client.post("/api/v1/auth/login", json={})
        assert response.status_code == 400

    @pytest.mark.unit
    def test_login_returns_400_when_username_missing(self, client: FlaskClient) -> None:
        response = client.post("/api/v1/auth/login", json={"password": "pass"})
        assert response.status_code == 400

    @pytest.mark.unit
    def test_login_returns_400_when_password_missing(self, client: FlaskClient) -> None:
        response = client.post("/api/v1/auth/login", json={"username": "user"})
        assert response.status_code == 400

    @pytest.mark.unit
    def test_login_returns_401_when_user_not_found(self, client: FlaskClient) -> None:
        with patch("src.controllers.auth_controller.UserService.get_user_by_username", return_value=None):
            response = client.post("/api/v1/auth/login", json={"username": "nobody", "password": "pass"})
        assert response.status_code == 401

    @pytest.mark.unit
    def test_login_returns_401_when_password_invalid(self, client: FlaskClient) -> None:
        mock_user: MagicMock = MagicMock()
        mock_user.password = EncryptService("correct").password_hashed
        with patch("src.controllers.auth_controller.UserService.get_user_by_username", return_value=mock_user):
            response = client.post("/api/v1/auth/login", json={"username": "user", "password": "wrong"})
        assert response.status_code == 401

    @pytest.mark.unit
    def test_login_returns_200_with_valid_credentials(self, client: FlaskClient) -> None:
        mock_user: MagicMock = MagicMock()
        mock_user.password = EncryptService("correctpass").password_hashed
        mock_user.is_active = True
        mock_user.is_authenticated = True
        mock_user.is_anonymous = False
        mock_user.get_id.return_value = "1"
        with patch("src.controllers.auth_controller.UserService.get_user_by_username", return_value=mock_user):
            response = client.post("/api/v1/auth/login", json={"username": "alice", "password": "correctpass"})
        assert response.status_code == 200

    @pytest.mark.unit
    def test_login_response_contains_redirect_to(self, client: FlaskClient) -> None:
        mock_user: MagicMock = MagicMock()
        mock_user.password = EncryptService("pass123").password_hashed
        mock_user.is_active = True
        mock_user.is_authenticated = True
        mock_user.is_anonymous = False
        mock_user.get_id.return_value = "1"
        with patch("src.controllers.auth_controller.UserService.get_user_by_username", return_value=mock_user):
            response = client.post("/api/v1/auth/login", json={"username": "alice", "password": "pass123"})
        data: dict = response.get_json()
        assert "redirect_to" in data


class TestAuthControllerLogout:
    @pytest.mark.unit
    def test_logout_returns_302_when_not_authenticated(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/auth/logout")
        assert response.status_code in (401, 302)

    @pytest.mark.integration
    def test_logout_returns_200_when_authenticated(self, app: Flask, auth_client: FlaskClient, db_session: None) -> None:
        response = auth_client.get("/api/v1/auth/logout")
        assert response.status_code == 200

    @pytest.mark.integration
    def test_logout_response_contains_redirect_to(self, app: Flask, auth_client: FlaskClient, db_session: None) -> None:
        response = auth_client.get("/api/v1/auth/logout")
        data: dict = response.get_json()
        assert "redirect_to" in data


class TestAuthControllerSignUp:
    @pytest.mark.unit
    def test_sign_up_returns_400_when_fields_missing(self, client: FlaskClient) -> None:
        response = client.post("/api/v1/auth/sign_up", json={})
        assert response.status_code == 400

    @pytest.mark.unit
    def test_sign_up_returns_400_when_email_missing(self, client: FlaskClient) -> None:
        response = client.post("/api/v1/auth/sign_up", json={"username": "u", "password": "p"})
        assert response.status_code == 400

    @pytest.mark.unit
    def test_sign_up_returns_409_when_username_exists(self, client: FlaskClient) -> None:
        existing_user: MagicMock = MagicMock()
        with patch("src.controllers.auth_controller.UserService.get_user_by_username", return_value=existing_user):
            with patch("src.controllers.auth_controller.UserService.get_user_by_email", return_value=None):
                response = client.post("/api/v1/auth/sign_up", json={"username": "taken", "password": "p", "email": "new@test.com"})
        assert response.status_code == 409

    @pytest.mark.unit
    def test_sign_up_returns_409_when_email_exists(self, client: FlaskClient) -> None:
        existing_user: MagicMock = MagicMock()
        with patch("src.controllers.auth_controller.UserService.get_user_by_username", return_value=None):
            with patch("src.controllers.auth_controller.UserService.get_user_by_email", return_value=existing_user):
                response = client.post("/api/v1/auth/sign_up", json={"username": "new", "password": "p", "email": "taken@test.com"})
        assert response.status_code == 409

    @pytest.mark.unit
    def test_sign_up_returns_201_with_new_user(self, client: FlaskClient) -> None:
        new_user: MagicMock = MagicMock()
        with patch("src.controllers.auth_controller.UserService.get_user_by_username", return_value=None):
            with patch("src.controllers.auth_controller.UserService.get_user_by_email", return_value=None):
                with patch("src.controllers.auth_controller.UserService.add_user", return_value=new_user):
                    response = client.post("/api/v1/auth/sign_up", json={"username": "newuser", "password": "pass", "email": "new@test.com"})
        assert response.status_code == 201
