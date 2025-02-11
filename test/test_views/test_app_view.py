import logging
import jinja2
from typing import Any
from typing import Generator

from flask import Flask
from flask import Response
from flask.testing import FlaskClient


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def test_home_view_without_login(flask_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any]) -> None:
    response: Response = flask_client.get(
        f"{blueprints['app_views']}/home",
        follow_redirects=False
    )

    status_code = response.status_code
    location = response.location

    assert status_code == 302
    assert location == f"{flask_app.config['LOGIN_VIEW_PATH']}?next={flask_app.config['HOME_VIEW_PATH'].replace('/', '%2F')}"
    

def test_home_view(authenticated_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], captured_templates: Generator[jinja2.environment.Template, None, dict[str, Any]]) -> None:
    response: Response = authenticated_client.get(
        f"{blueprints['app_views']}/home",
        follow_redirects=False
    )

    template, context = captured_templates[0]

    status_code = response.status_code
    template_name = template.name

    assert status_code == 200
    assert template_name == flask_app.config["TEMPLATE_HOME_NAME"]