from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_handle_exceptions_base_api_error(error_app: FlaskClient) -> None:
    res: TestResponse = error_app.get("/base-api-error", follow_redirects=False)

    assert res.status_code == 302
    assert res.headers["Location"].endswith("/base-api-error")


def test_handle_exceptions_sql_error(error_app: FlaskClient) -> None:
    res: TestResponse = error_app.get("/sql-error", follow_redirects=False)

    assert res.status_code == 302
    assert res.headers["Location"].endswith("/sql-error")


def test_handle_exceptions_generic_error(error_app: FlaskClient) -> None:
    res: TestResponse = error_app.get("/generic-error", follow_redirects=False)

    assert res.status_code == 302
    assert res.headers["Location"].endswith("/generic-error")


def test_handle_exceptions_no_error(error_app: FlaskClient) -> None:
    res: TestResponse = error_app.get("/no-error", follow_redirects=False)
    body = res.get_json()

    assert res.status_code == 200
    assert body["ok"] is True
