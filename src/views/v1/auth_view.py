from flask import Blueprint, Response, current_app, redirect, render_template, url_for
from flask_login import current_user

from src.constants.paths import RENDER_TEMPLATE_LOGIN_PATH, RENDER_TEMPLATE_SIGN_UP_PATH
from src.utils.helpers import get_context_by_key

auth_view = Blueprint("auth_view", __name__, template_folder="templates")


@auth_view.before_request
def before_request():
    if current_app.config["TESTING"]:
        return

    if current_user.is_authenticated:
        return redirect(url_for(current_app.config["HOME_VIEW"]))


@auth_view.route("/login", methods=["GET"])
def login() -> Response:
    context = get_context_by_key(app=current_app, key="login")

    return render_template(RENDER_TEMPLATE_LOGIN_PATH, context=context)


@auth_view.route("/sign_up", methods=["GET"])
def sign_up() -> Response:
    context = get_context_by_key(app=current_app, key="register")

    return render_template(RENDER_TEMPLATE_SIGN_UP_PATH, context=context)
