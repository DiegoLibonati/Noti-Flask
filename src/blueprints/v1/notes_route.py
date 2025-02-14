from flask import Response
from flask import Blueprint
from flask_login import login_required

from src.controllers import notes_controller


notes_route = Blueprint("notes_route", __name__)


@notes_route.route("/create", methods = ["POST"])
@login_required
def create() -> Response:
    return notes_controller.create()

@notes_route.route("/delete/<id>", methods = ["DELETE"])
@login_required
def delete(id: str) -> Response:
    return notes_controller.delete(id=id)