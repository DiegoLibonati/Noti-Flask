from flask import Blueprint

from src.controllers.auth_controller import alive, login, logout, sign_up

auth_bp = Blueprint("auth", __name__)

auth_bp.route("/alive", methods=["GET"])(alive)
auth_bp.route("/logout", methods=["GET"])(logout)
auth_bp.route("/login", methods=["POST"])(login)
auth_bp.route("/sign_up", methods=["POST"])(sign_up)
