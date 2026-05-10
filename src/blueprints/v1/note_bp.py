from flask import Blueprint

from src.controllers.note_controller import alive, create, delete, edit, get_all

note_bp = Blueprint("notes", __name__)

note_bp.route("/alive", methods=["GET"])(alive)
note_bp.route("/", methods=["GET"])(get_all)
note_bp.route("/", methods=["POST"])(create)
note_bp.route("/<id>", methods=["DELETE"])(delete)
note_bp.route("/<id>", methods=["PATCH"])(edit)
