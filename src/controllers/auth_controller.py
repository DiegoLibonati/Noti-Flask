from flask import Response, current_app, flash, jsonify, redirect, request, url_for
from flask_login import login_required, login_user, logout_user

from config.logger_config import setup_logger
from src.constants.codes import FLASH_ERROR, FLASH_SUCCESS
from src.constants.messages import (
    MESSAGE_ALREADY_USER_EXISTS,
    MESSAGE_NOT_EXISTS_USER,
    MESSAGE_NOT_VALID_FIELDS,
    MESSAGE_NOT_VALID_PASSWORD,
    MESSAGE_SUCCESFULLY_LOGGED_IN,
    MESSAGE_SUCCESFULLY_LOGOUT,
    MESSAGE_SUCCESFULLY_SIGN_UP,
)
from src.models.orm.user import User
from src.services.encrypt_service import EncryptService
from src.services.user_service import UserService
from src.utils.error_handler import handle_exceptions

logger = setup_logger()


@handle_exceptions
def alive() -> Response:
    response = {
        "message": "I am Alive!",
        "version_bp": "2.0.0",
        "author": "Diego Libonati",
        "name_bp": "Auth",
    }

    return jsonify(response), 200


@handle_exceptions
def login() -> Response:
    body = request.form

    username = body.get("username", "").strip()
    password = body.get("password", "").strip()

    if not username or not password:
        flash(MESSAGE_NOT_VALID_FIELDS, FLASH_ERROR)
        return redirect(url_for(current_app.config["LOGIN_VIEW"]))

    user = UserService.get_user_by_username(username=username)

    if not user:
        flash(MESSAGE_NOT_EXISTS_USER, FLASH_ERROR)
        return redirect(url_for(current_app.config["LOGIN_VIEW"]))

    if not EncryptService(password).valid_password(user.password):
        flash(MESSAGE_NOT_VALID_PASSWORD, FLASH_ERROR)
        return redirect(url_for(current_app.config["LOGIN_VIEW"]))

    login_user(user=user, remember=True)

    flash(MESSAGE_SUCCESFULLY_LOGGED_IN, FLASH_SUCCESS)
    return redirect(url_for(current_app.config["HOME_VIEW"]))


@login_required
@handle_exceptions
def logout() -> Response:
    logout_user()

    flash(MESSAGE_SUCCESFULLY_LOGOUT, FLASH_SUCCESS)
    return redirect(url_for(current_app.config["LOGIN_VIEW"]))


@handle_exceptions
def sign_up() -> Response:
    body = request.form

    username = body.get("username", "").strip()
    password = body.get("password", "").strip()
    email = body.get("email", "").strip()

    if not username or not password or not email:
        flash(MESSAGE_NOT_VALID_FIELDS, FLASH_ERROR)
        return redirect(url_for(current_app.config["SIGN_UP_VIEW"]))

    username_exists = UserService.get_user_by_username(username=username)
    email_exists = UserService.get_user_by_email(email=email)

    if email_exists or username_exists:
        flash(MESSAGE_ALREADY_USER_EXISTS, FLASH_ERROR)
        return redirect(url_for(current_app.config["SIGN_UP_VIEW"]))

    UserService.add_user(
        User(
            username=username,
            password=EncryptService(password).password_hashed,
            email=email,
        )
    )

    flash(MESSAGE_SUCCESFULLY_SIGN_UP, FLASH_SUCCESS)
    return redirect(url_for(current_app.config["LOGIN_VIEW"]))
