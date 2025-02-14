import logging
import jinja2
from typing import Any
from typing import Generator

import pytest

from flask import Flask
from flask import template_rendered
from flask_login import login_user
from flask.testing import FlaskClient

from src.app import app as api_app
from src.data_access.user_repository import UserRepository
from src.data_access.note_repository import NoteRepository
from src.models.db.User import User
from test.constants import MOCK_USER
from test.constants import BLUEPRINTS


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# APP CONFIG

@pytest.fixture(scope="session")
def flask_app() -> Flask:
    app = api_app
    
    with app.app_context(): 
        yield app


@pytest.fixture(scope="session")
def flask_client(flask_app: Flask) -> FlaskClient:
    return flask_app.test_client()


@pytest.fixture(scope="session")
def authenticated_client(flask_client: FlaskClient, flask_app: Flask) -> FlaskClient:
    """Fixture que autentica un usuario de prueba en la app Flask."""
    with flask_app.test_request_context():
        user = User(id=1)
        login_user(user=user)

    return flask_client


@pytest.fixture(scope="session")
def blueprints() -> dict[str, Any]:
    return BLUEPRINTS


@pytest.fixture(scope="session")
def user_repository() -> UserRepository:
    return UserRepository()


@pytest.fixture(scope="session")
def note_repository() -> NoteRepository:
    return NoteRepository()


@pytest.fixture
def captured_templates(flask_app: Flask) -> Generator[jinja2.environment.Template, None, dict[str, Any]]:
    recorded = []

    def record(sender: Flask, template: jinja2.environment.Template, context: dict[str, Any], **extra: dict[str, Any]):
        recorded.append((template, context))

    template_rendered.connect(record, flask_app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, flask_app)


# MOCKS

@pytest.fixture(scope="session")
def mock_user() -> dict[str, Any]:
    return MOCK_USER
