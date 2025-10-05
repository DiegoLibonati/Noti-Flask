from flask import Blueprint

from src.controllers.note_controller import alive, create, delete, edit

note_bp = Blueprint("note", __name__)

note_bp.route("/alive", methods=["GET"])(alive)
note_bp.route("/", methods=["POST"])(create)
note_bp.route("/<id>", methods=["DELETE"])(delete)
note_bp.route("/<id>", methods=["PATCH"])(edit)
