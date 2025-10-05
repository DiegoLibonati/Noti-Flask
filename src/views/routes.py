from flask import Flask

from src.constants.vars import VIEW_APP_PATH, VIEW_AUTH_PATH
from src.views.v1.app_view import app_view
from src.views.v1.auth_view import auth_view


def register_views(app: Flask) -> None:
    app.register_blueprint(app_view, url_prefix=VIEW_APP_PATH)
    app.register_blueprint(auth_view, url_prefix=VIEW_AUTH_PATH)
