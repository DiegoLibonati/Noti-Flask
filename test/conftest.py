import subprocess
import time
import uuid
from test.constants import COMPOSE_FILE
from typing import Any, Generator

import jinja2
import pytest
from flask import Blueprint, Flask, jsonify, template_rendered
from flask.testing import FlaskClient
from flask_login import login_user
from sqlalchemy.exc import SQLAlchemyError

from config.sql_alchemy_config import db
from src import create_app
from src.models.orm.note import Note
from src.models.orm.user import User
from src.utils.error_handler import handle_exceptions
from src.utils.exceptions import ValidationAPIError


@pytest.fixture(scope="session")
def flask_app(sql_test_db: None) -> Flask:
    app = create_app("testing")
    return app


@pytest.fixture(scope="session")
def flask_client(flask_app: Flask) -> FlaskClient:
    return flask_app.test_client()


@pytest.fixture
def authenticated_client(flask_app: Flask) -> FlaskClient:
    client: FlaskClient = flask_app.test_client()

    with flask_app.test_request_context():
        user = User(id=1)
        login_user(user)

    return client


@pytest.fixture(scope="session", autouse=True)
def setup_database(flask_app: Flask):
    with flask_app.app_context():
        db.create_all()
        yield
        db.drop_all()


@pytest.fixture(autouse=True)
def clean_database(flask_app: Flask) -> None:
    with flask_app.app_context():
        db.session.query(Note).delete()
        db.session.query(User).delete()
        db.session.commit()


@pytest.fixture
def error_app() -> FlaskClient:
    app = create_app("testing")

    bp = Blueprint("test_errors", __name__)

    @bp.route("/base-api-error")
    @handle_exceptions
    def raise_base_api_error() -> None:
        raise ValidationAPIError()

    @bp.route("/sql-error")
    @handle_exceptions
    def raise_sql_error() -> None:
        raise SQLAlchemyError("Database connection failed")

    @bp.route("/generic-error")
    @handle_exceptions
    def raise_generic_error() -> None:
        raise RuntimeError("Unexpected failure")

    @bp.route("/no-error")
    @handle_exceptions
    def no_error():
        return jsonify({"ok": True})

    app.register_blueprint(bp)
    return app.test_client()


@pytest.fixture(scope="session")
def sql_test_db() -> None:
    subprocess.run(
        ["docker-compose", "-f", COMPOSE_FILE, "up", "-d", "noti-db"],
        check=True,
    )

    time.sleep(5)

    yield

    subprocess.run(
        ["docker-compose", "-f", COMPOSE_FILE, "down"],
        check=True,
    )


@pytest.fixture
def captured_templates(
    flask_app: Flask,
) -> Generator[jinja2.environment.Template, None, dict[str, Any]]:
    recorded = []

    def record(
        sender: Flask,
        template: jinja2.environment.Template,
        context: dict[str, Any],
        **extra: dict[str, Any],
    ):
        recorded.append((template, context))

    template_rendered.connect(record, flask_app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, flask_app)


@pytest.fixture
def unique_user() -> dict[str, Any]:
    return {"username": "test_user", "password": "1234", "email": "user_test@gmail.com"}


@pytest.fixture
def unique_note() -> dict[str, Any]:
    return {
        "id": 1,
        "content": f"test_note_{uuid.uuid4().hex[:6]}",
        "user_id": 1,
    }
