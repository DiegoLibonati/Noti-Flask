from flask import Response, current_app, flash, jsonify, request
from flask_login import login_required, login_user, logout_user

from src.configs.logger_config import setup_logger
from src.constants.codes import (
    CODE_ALREADY_EXISTS_USER,
    CODE_NOT_FOUND_USER,
    CODE_NOT_VALID_FIELDS,
    CODE_NOT_VALID_PASSWORD,
    CODE_SUCCESS_LOGGED_IN,
    CODE_SUCCESS_LOGOUT,
    CODE_SUCCESS_SIGN_UP,
    FLASH_ERROR,
    FLASH_SUCCESS,
)
from src.constants.messages import (
    MESSAGE_ALREADY_EXISTS_USER,
    MESSAGE_NOT_FOUND_USER,
    MESSAGE_NOT_VALID_FIELDS,
    MESSAGE_NOT_VALID_PASSWORD,
    MESSAGE_SUCCESS_LOGGED_IN,
    MESSAGE_SUCCESS_LOGOUT,
    MESSAGE_SUCCESS_SIGN_UP,
)
from src.models.orm.user import User
from src.services.encrypt_service import EncryptService
from src.services.user_service import UserService
from src.utils.error_handler import handle_exceptions
from src.utils.exceptions import AuthenticationAPIError, ConflictAPIError, ValidationAPIError

logger = setup_logger()


@handle_exceptions
def alive() -> Response:
    response = {
        "message": "I am Alive!",
        "version_bp": "1.0.0",
        "name_bp": "Auth",
    }
    return jsonify(response), 200


@handle_exceptions
def login() -> Response:
    body = request.get_json(silent=True) or {}

    username = body.get("username", "").strip()
    password = body.get("password", "").strip()

    if not username or not password:
        flash(MESSAGE_NOT_VALID_FIELDS, FLASH_ERROR)
        raise ValidationAPIError(code=CODE_NOT_VALID_FIELDS, message=MESSAGE_NOT_VALID_FIELDS)

    user = UserService.get_user_by_username(username=username)

    if not user:
        flash(MESSAGE_NOT_FOUND_USER, FLASH_ERROR)
        raise AuthenticationAPIError(code=CODE_NOT_FOUND_USER, message=MESSAGE_NOT_FOUND_USER)

    if not EncryptService(password).valid_password(user.password):
        flash(MESSAGE_NOT_VALID_PASSWORD, FLASH_ERROR)
        raise AuthenticationAPIError(code=CODE_NOT_VALID_PASSWORD, message=MESSAGE_NOT_VALID_PASSWORD)

    login_user(user=user, remember=True)

    flash(MESSAGE_SUCCESS_LOGGED_IN, FLASH_SUCCESS)
    response = {
        "code": CODE_SUCCESS_LOGGED_IN,
        "message": MESSAGE_SUCCESS_LOGGED_IN,
        "redirect_to": current_app.config["HOME_VIEW_PATH"],
    }
    return jsonify(response), 200


@login_required
@handle_exceptions
def logout() -> Response:
    logout_user()

    flash(MESSAGE_SUCCESS_LOGOUT, FLASH_SUCCESS)
    response = {
        "code": CODE_SUCCESS_LOGOUT,
        "message": MESSAGE_SUCCESS_LOGOUT,
        "redirect_to": current_app.config["LOGIN_VIEW_PATH"],
    }
    return jsonify(response), 200


@handle_exceptions
def sign_up() -> Response:
    body = request.get_json(silent=True) or {}

    username = body.get("username", "").strip()
    password = body.get("password", "").strip()
    email = body.get("email", "").strip()

    if not username or not password or not email:
        flash(MESSAGE_NOT_VALID_FIELDS, FLASH_ERROR)
        raise ValidationAPIError(code=CODE_NOT_VALID_FIELDS, message=MESSAGE_NOT_VALID_FIELDS)

    username_exists = UserService.get_user_by_username(username=username)
    email_exists = UserService.get_user_by_email(email=email)

    if email_exists or username_exists:
        flash(MESSAGE_ALREADY_EXISTS_USER, FLASH_ERROR)
        raise ConflictAPIError(code=CODE_ALREADY_EXISTS_USER, message=MESSAGE_ALREADY_EXISTS_USER)

    UserService.add_user(
        User(
            username=username,
            password=EncryptService(password).password_hashed,
            email=email,
        )
    )

    flash(MESSAGE_SUCCESS_SIGN_UP, FLASH_SUCCESS)
    response = {
        "code": CODE_SUCCESS_SIGN_UP,
        "message": MESSAGE_SUCCESS_SIGN_UP,
        "redirect_to": current_app.config["LOGIN_VIEW_PATH"],
    }
    return jsonify(response), 201
