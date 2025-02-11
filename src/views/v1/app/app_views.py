from flask import Blueprint
from flask import Response
from flask import render_template
from flask import current_app
from flask_login import login_required


app_views = Blueprint("app_views", __name__, template_folder="templates")

@app_views.route("/home", methods = ["GET"])
@login_required
def home() -> Response:
    return render_template(current_app.config["TEMPLATE_HOME_NAME"])