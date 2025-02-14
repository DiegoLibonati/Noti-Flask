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


def test_home_view_without_login(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any]) -> None:

    with patch("flask_login.utils._get_user", return_value=AnonymousUserMixin()):
        response: Response = flask_client.get(f"{blueprints['app_views']}/home", follow_redirects=False)

    status_code = response.status_code
    location = response.location

    assert status_code == 302
    assert location == f"{flask_app.config['LOGIN_VIEW_PATH']}?next={flask_app.config['HOME_VIEW_PATH'].replace('/', '%2F')}"
    

def test_home_view(authenticated_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], captured_templates: Generator[jinja2.environment.Template, None, dict[str, Any]]) -> None:
    context = get_context_by_key(app=flask_app, key="home")

    response: Response = authenticated_client.get(
        f"{blueprints['app_views']}/home",
        follow_redirects=False
    )

    template, template_config = captured_templates[0]

    status_code = response.status_code
    template_name = template.name

    assert status_code == 200
    assert template_name == flask_app.config["TEMPLATE_HOME_NAME"]
    assert context == template_config.get("context")