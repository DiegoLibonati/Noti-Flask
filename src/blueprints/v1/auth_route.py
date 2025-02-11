from flask import Response
from flask import Blueprint
from flask_login import login_required

from src.controllers import auth_controller


auth_route = Blueprint("auth_route", __name__)


@auth_route.route("/login", methods = ["POST"])
def login() -> Response:
    return auth_controller.login()


@auth_route.route("/logout", methods = ["GET"])
@login_required
def logout() -> Response:
    return auth_controller.logout()


@auth_route.route("/sign_up", methods = ["POST"])
def sign_up() -> Response:
    return auth_controller.sign_up()