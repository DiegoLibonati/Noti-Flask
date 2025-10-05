from flask import Blueprint, Response, current_app, render_template
from flask_login import login_required

from src.constants.paths import RENDER_TEMPLATE_HOME_PATH
from src.utils.helpers import get_context_by_key

app_view = Blueprint("app_view", __name__, template_folder="templates")


@app_view.route("/home", methods=["GET"])
@login_required
def home() -> Response:
    context = get_context_by_key(app=current_app, key="home")

    return render_template(RENDER_TEMPLATE_HOME_PATH, context=context)
