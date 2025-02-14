import logging
from typing import Any

from flask import Flask
from flask import Response
from flask.testing import FlaskClient


from src.data_access.user_repository import UserRepository
from src.utils.constants import FLASH_ERROR
from src.utils.constants import FLASH_SUCCESS
from src.utils.constants import CODE_NOT_VALID_FIELDS
from src.utils.constants import CODE_NOT_EXISTS_USER
from src.utils.constants import CODE_NOT_VALID_PASSWORD
from src.utils.constants import CODE_ALREADY_USER_EXISTS
from src.utils.constants import CODE_SUCCESFULLY_LOGGED_IN
from src.utils.constants import CODE_SUCCESFULLY_SIGN_UP
from src.utils.constants import CODE_SUCCESFULLY_LOGOUT
from src.utils.constants import MESSAGE_NOT_VALID_FIELDS
from src.utils.constants import MESSAGE_NOT_EXISTS_USER
from src.utils.constants import MESSAGE_NOT_VALID_PASSWORD
from src.utils.constants import MESSAGE_SUCCESFULLY_LOGGED_IN
from src.utils.constants import MESSAGE_SUCCESFULLY_SIGN_UP
from src.utils.constants import MESSAGE_SUCCESFULLY_LOGOUT
from src.utils.constants import MESSAGE_ALREADY_USER_EXISTS


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def test_sign_up_invalid_fields(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], user_repository: UserRepository, mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")
    password = ""
    email = mock_user.get("email")

    response: Response = flask_client.post(
        f"{blueprints['auth']}/sign_up",
        json={
            "username": username,
            "password": password,
            "email": email
        }
    )

    status_code = response.status_code
    data = response.get_json()

    assert status_code == 400
    assert data.get("message") == MESSAGE_NOT_VALID_FIELDS
    assert data.get("code") == CODE_NOT_VALID_FIELDS
    assert data.get("redirect_to") == flask_app.config["SIGN_UP_VIEW_PATH"]

    with flask_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert (FLASH_ERROR, MESSAGE_NOT_VALID_FIELDS) in flashes

    user_exists = user_repository.get_user_by_username(username=username)

    assert not user_exists


def test_sign_up(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], user_repository: UserRepository, mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")
    password = mock_user.get("password")
    email = mock_user.get("email")

    response: Response = flask_client.post(
        f"{blueprints['auth']}/sign_up",
        json={
            "username": username,
            "password": password,
            "email": email
        }
    )

    status_code = response.status_code
    data = response.get_json()

    assert status_code == 201
    assert data.get("message") == MESSAGE_SUCCESFULLY_SIGN_UP
    assert data.get("code") == CODE_SUCCESFULLY_SIGN_UP
    assert data.get("redirect_to") == flask_app.config["LOGIN_VIEW_PATH"]

    with flask_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert (FLASH_SUCCESS, MESSAGE_SUCCESFULLY_SIGN_UP) in flashes


    user_exists = user_repository.get_user_by_username(username=username)

    assert user_exists


def test_sign_up_already_exists(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], user_repository: UserRepository, mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")
    password = mock_user.get("password")
    email = mock_user.get("email")

    response: Response = flask_client.post(
        f"{blueprints['auth']}/sign_up",
        json={
            "username": username,
            "password": password,
            "email": email
        }
    )

    status_code = response.status_code
    data = response.get_json()

    assert status_code == 400
    assert data.get("message") == MESSAGE_ALREADY_USER_EXISTS
    assert data.get("code") == CODE_ALREADY_USER_EXISTS
    assert data.get("redirect_to") == flask_app.config["SIGN_UP_VIEW_PATH"]

    with flask_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert (FLASH_ERROR, MESSAGE_ALREADY_USER_EXISTS) in flashes


    user_exists = user_repository.get_user_by_username(username=username)

    assert user_exists


def test_login_invalid_fields(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")
    password = ""

    response: Response = flask_client.post(
        f"{blueprints['auth']}/login",
        json={
            "username": username,
            "password": password,
        }
    )

    status_code = response.status_code
    data = response.get_json()

    assert status_code == 400
    assert data.get("message") == MESSAGE_NOT_VALID_FIELDS
    assert data.get("code") == CODE_NOT_VALID_FIELDS
    assert data.get("redirect_to") == flask_app.config["LOGIN_VIEW_PATH"]

    with flask_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert (FLASH_ERROR, MESSAGE_NOT_VALID_FIELDS) in flashes


def test_login_user_not_exists(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username") + "1234"
    password = mock_user.get("password")

    response: Response = flask_client.post(
        f"{blueprints['auth']}/login",
        json={
            "username": username,
            "password": password,
        }
    )

    status_code = response.status_code
    data = response.get_json()

    assert status_code == 404
    assert data.get("message") == MESSAGE_NOT_EXISTS_USER
    assert data.get("code") == CODE_NOT_EXISTS_USER
    assert data.get("redirect_to") == flask_app.config["LOGIN_VIEW_PATH"]

    with flask_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert (FLASH_ERROR, MESSAGE_NOT_EXISTS_USER) in flashes


def test_login_invalid_password(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")
    password = mock_user.get("password") + "1234"

    response: Response = flask_client.post(
        f"{blueprints['auth']}/login",
        json={
            "username": username,
            "password": password,
        }
    )

    status_code = response.status_code
    data = response.get_json()

    assert status_code == 400
    assert data.get("message") == MESSAGE_NOT_VALID_PASSWORD
    assert data.get("code") == CODE_NOT_VALID_PASSWORD
    assert data.get("redirect_to") == flask_app.config["LOGIN_VIEW_PATH"]

    with flask_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert (FLASH_ERROR, MESSAGE_NOT_VALID_PASSWORD) in flashes


def test_login(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], user_repository: UserRepository, mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")
    password = mock_user.get("password")

    response: Response = flask_client.post(
        f"{blueprints['auth']}/login",
        json={
            "username": username,
            "password": password,
        }
    )

    status_code = response.status_code
    data = response.get_json()

    assert status_code == 200
    assert data.get("message") == MESSAGE_SUCCESFULLY_LOGGED_IN
    assert data.get("code") == CODE_SUCCESFULLY_LOGGED_IN
    assert data.get("redirect_to") == flask_app.config["HOME_VIEW_PATH"]

    with flask_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert (FLASH_SUCCESS, MESSAGE_SUCCESFULLY_LOGGED_IN) in flashes


def test_logout(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any]) -> None:
    response: Response = flask_client.get(
        f"{blueprints['auth']}/logout"
    )

    status_code = response.status_code
    data = response.get_json()

    assert status_code == 200
    assert data.get("message") == MESSAGE_SUCCESFULLY_LOGOUT
    assert data.get("code") == CODE_SUCCESFULLY_LOGOUT
    assert data.get("redirect_to") == flask_app.config["LOGIN_VIEW_PATH"]

    with flask_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert (FLASH_SUCCESS, MESSAGE_SUCCESFULLY_LOGOUT) in flashes


def test_delete_test_user(mock_user: dict[str, Any], user_repository: UserRepository) -> None:
    username = mock_user.get("username")

    user = user_repository.get_user_by_username(username=username)

    assert user

    remove = user_repository.remove_user(user=user)

    assert remove