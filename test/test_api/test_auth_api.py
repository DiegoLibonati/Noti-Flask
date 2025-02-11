import logging
from typing import Any

from flask import Flask
from flask import Response
from flask.testing import FlaskClient


from src.data_access.user_repository import UserRepository


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def test_sign_up_invalid_fields(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], user_repository: UserRepository, mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")
    password = ""
    email = mock_user.get("email")

    response: Response = flask_client.post(
        f"{blueprints['auth']}/sign_up",
        data={
            "username": username,
            "password": password,
            "email": email
        },
        follow_redirects=False
    )

    status_code = response.status_code
    location = response.location

    assert status_code == 302
    assert location == flask_app.config["SIGN_UP_VIEW_PATH"]

    with flask_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert ("error", "You must enter valid fields to register.") in flashes

    user_exists = user_repository.get_user_by_username(username=username)

    assert not user_exists


def test_sign_up(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], user_repository: UserRepository, mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")
    password = mock_user.get("password")
    email = mock_user.get("email")

    response: Response = flask_client.post(
        f"{blueprints['auth']}/sign_up",
        data={
            "username": username,
            "password": password,
            "email": email
        },
        follow_redirects=False
    )

    status_code = response.status_code
    location = response.location

    assert status_code == 302
    assert location == flask_app.config["LOGIN_VIEW_PATH"]

    with flask_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert ("success", "Your account was successfully created.") in flashes


    user_exists = user_repository.get_user_by_username(username=username)

    assert user_exists


def test_sign_up_already_exists(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], user_repository: UserRepository, mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")
    password = mock_user.get("password")
    email = mock_user.get("email")

    response: Response = flask_client.post(
        f"{blueprints['auth']}/sign_up",
        data={
            "username": username,
            "password": password,
            "email": email
        },
        follow_redirects=False
    )

    status_code = response.status_code
    location = response.location

    assert status_code == 302
    assert location == flask_app.config["SIGN_UP_VIEW_PATH"]

    with flask_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert ("error", "The entered email or username already exists.") in flashes


    user_exists = user_repository.get_user_by_username(username=username)

    assert user_exists


def test_login_invalid_fields(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")
    password = ""

    response: Response = flask_client.post(
        f"{blueprints['auth']}/login",
        data={
            "username": username,
            "password": password,
        },
        follow_redirects=False
    )

    status_code = response.status_code
    location = response.location

    assert status_code == 302
    assert location == flask_app.config["LOGIN_VIEW_PATH"]

    with flask_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert ("error", "You must enter valid fields to login.") in flashes


def test_login_user_not_exists(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username") + "1234"
    password = mock_user.get("password")

    response: Response = flask_client.post(
        f"{blueprints['auth']}/login",
        data={
            "username": username,
            "password": password,
        },
        follow_redirects=False
    )

    status_code = response.status_code
    location = response.location

    assert status_code == 302
    assert location == flask_app.config["LOGIN_VIEW_PATH"]

    with flask_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert ("error", "There is no account with the entered username.") in flashes


def test_login_invalid_password(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")
    password = mock_user.get("password") + "1234"

    response: Response = flask_client.post(
        f"{blueprints['auth']}/login",
        data={
            "username": username,
            "password": password,
        },
        follow_redirects=False
    )

    status_code = response.status_code
    location = response.location

    assert status_code == 302
    assert location == flask_app.config["LOGIN_VIEW_PATH"]

    with flask_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert ("error", "The password entered is not valid.") in flashes


def test_login(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], user_repository: UserRepository, mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")
    password = mock_user.get("password")

    response: Response = flask_client.post(
        f"{blueprints['auth']}/login",
        data={
            "username": username,
            "password": password,
        },
        follow_redirects=False
    )

    status_code = response.status_code
    location = response.location

    assert status_code == 302
    assert location == flask_app.config["HOME_VIEW_PATH"]

    with flask_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert ("success", "You have successfully logged in.") in flashes


def test_logout(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any]) -> None:
    response: Response = flask_client.get(
        f"{blueprints['auth']}/logout",
        follow_redirects=False
    )

    status_code = response.status_code
    location = response.location

    assert status_code == 302
    assert location == flask_app.config["LOGIN_VIEW_PATH"]

    with flask_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert ("success", "You have successfully disconnected.") in flashes


def test_delete_test_user(mock_user: dict[str, Any], user_repository: UserRepository) -> None:
    username = mock_user.get("username")

    user = user_repository.get_user_by_username(username=username)

    assert user

    remove = user_repository.remove_user(user=user)

    assert remove