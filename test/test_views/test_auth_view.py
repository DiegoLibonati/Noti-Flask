from unittest.mock import patch

import logging
import jinja2
from typing import Any
from typing import Generator

from flask import Flask
from flask import Response
from flask.testing import FlaskClient
from flask_login import AnonymousUserMixin

from src.utils.utils import get_context_by_key


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def test_login_view(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], captured_templates: Generator[jinja2.environment.Template, None, dict[str, Any]]) -> None:
    context = get_context_by_key(app=flask_app, key="login")

    with patch("flask_login.utils._get_user", return_value=AnonymousUserMixin()):
        response: Response = flask_client.get(f"{blueprints['auth_views']}/login", follow_redirects=False)

    template, template_config = captured_templates[0]

    status_code = response.status_code
    template_name = template.name

    assert status_code == 200
    assert template_name == flask_app.config["TEMPLATE_LOGIN_NAME"]
    assert context == template_config.get("context")


def test_sign_up_view(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], captured_templates: Generator[jinja2.environment.Template, None, dict[str, Any]]) -> None:
    context = get_context_by_key(app=flask_app, key="register")

    with patch("flask_login.utils._get_user", return_value=AnonymousUserMixin()):
        response: Response = flask_client.get(f"{blueprints['auth_views']}/sign_up", follow_redirects=False)

    template, template_config = captured_templates[0]

    status_code = response.status_code
    template_name = template.name

    assert status_code == 200
    assert template_name == flask_app.config["TEMPLATE_SIGN_UP_NAME"]
    assert context == template_config.get("context")