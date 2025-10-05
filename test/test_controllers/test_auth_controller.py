from test.constants import BLUEPRINTS
from typing import Any

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_alive(flask_client: FlaskClient) -> None:
    res: TestResponse = flask_client.get(f"{BLUEPRINTS['auth']}/alive")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 200
    assert body["name_bp"] == "Auth"
    assert body["message"] == "I am Alive!"


def test_sign_up_missing_fields(flask_client: FlaskClient) -> None:
    res: TestResponse = flask_client.post(
        f"{BLUEPRINTS['auth']}/sign_up",
        data={"username": "", "password": "", "email": ""},
        follow_redirects=False,
    )

    assert res.status_code == 302
    assert "/sign_up" in res.headers["Location"]


def test_sign_up_success(
    flask_client: FlaskClient, unique_user: dict[str, Any]
) -> None:
    res: TestResponse = flask_client.post(
        f"{BLUEPRINTS['auth']}/sign_up", data=unique_user, follow_redirects=False
    )

    assert res.status_code == 302
    assert "/login" in res.headers["Location"]


def test_sign_up_conflict(
    flask_client: FlaskClient, unique_user: dict[str, Any]
) -> None:
    flask_client.post(f"{BLUEPRINTS['auth']}/sign_up", data=unique_user)
    res: TestResponse = flask_client.post(
        f"{BLUEPRINTS['auth']}/sign_up", data=unique_user, follow_redirects=False
    )

    assert res.status_code == 302
    assert "/sign_up" in res.headers["Location"]


def test_login_user_not_exists(flask_client: FlaskClient) -> None:
    res: TestResponse = flask_client.post(
        f"{BLUEPRINTS['auth']}/login",
        data={"username": "ghost", "password": "1234"},
        follow_redirects=False,
    )

    assert res.status_code == 302
    assert "/login" in res.headers["Location"]


def test_login_wrong_password(
    flask_client: FlaskClient, unique_user: dict[str, Any]
) -> None:
    flask_client.post(f"{BLUEPRINTS['auth']}/sign_up", data=unique_user)
    res: TestResponse = flask_client.post(
        f"{BLUEPRINTS['auth']}/login",
        data={"username": unique_user["username"], "password": "wrong"},
        follow_redirects=False,
    )

    assert res.status_code == 302
    assert "/login" in res.headers["Location"]


def test_login_success(flask_client: FlaskClient, unique_user: dict[str, Any]) -> None:
    flask_client.post(f"{BLUEPRINTS['auth']}/sign_up", data=unique_user)
    res: TestResponse = flask_client.post(
        f"{BLUEPRINTS['auth']}/login",
        data={"username": unique_user["username"], "password": unique_user["password"]},
        follow_redirects=False,
    )

    assert res.status_code == 302
    assert "/home" in res.headers["Location"]


def test_logout_success(authenticated_client: FlaskClient) -> None:
    res: TestResponse = authenticated_client.get(
        f"{BLUEPRINTS['auth']}/logout", follow_redirects=False
    )

    assert res.status_code == 302
    assert "/login" in res.headers["Location"]
