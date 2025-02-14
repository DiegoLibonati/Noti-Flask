from flask import Blueprint
from flask import Response
from flask import render_template
from flask import current_app
from flask import redirect
from flask import url_for
from flask_login import current_user

from src.utils.utils import get_context_by_key


auth_views = Blueprint("auth_views", __name__, template_folder="templates")


@auth_views.before_request
def before_request():
    if current_app.config["TESTING"]:
        return

    if current_user.is_authenticated:
        return redirect(url_for(current_app.config["HOME_VIEW"]))
    

@auth_views.route("/login", methods = ["GET"])
def login() -> Response:
    context = get_context_by_key(app=current_app, key="login")

    return render_template(current_app.config["TEMPLATE_LOGIN_NAME"], context=context)


@auth_views.route("/sign_up", methods = ["GET"])
def sign_up() -> Response:
    context = get_context_by_key(app=current_app, key="register")

    return render_template(current_app.config["TEMPLATE_SIGN_UP_NAME"], context=context)