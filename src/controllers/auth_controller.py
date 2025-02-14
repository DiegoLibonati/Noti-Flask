import logging

from flask import Response
from flask import request
from flask import current_app
from flask import flash
from flask import make_response
from flask_login import login_user
from flask_login import logout_user
from werkzeug.security import check_password_hash

from src.data_access.user_repository import UserRepository
from src.utils.constants import FLASH_SUCCESS
from src.utils.constants import FLASH_ERROR
from src.utils.constants import CODE_SUCCESFULLY_LOGGED_IN
from src.utils.constants import CODE_SUCCESFULLY_LOGOUT
from src.utils.constants import CODE_SUCCESFULLY_SIGN_UP
from src.utils.constants import CODE_ALREADY_USER_EXISTS
from src.utils.constants import CODE_NOT_VALID_FIELDS
from src.utils.constants import CODE_NOT_EXISTS_USER
from src.utils.constants import CODE_NOT_VALID_PASSWORD
from src.utils.constants import MESSAGE_SUCCESFULLY_LOGGED_IN
from src.utils.constants import MESSAGE_SUCCESFULLY_LOGOUT
from src.utils.constants import MESSAGE_SUCCESFULLY_SIGN_UP
from src.utils.constants import MESSAGE_ALREADY_USER_EXISTS
from src.utils.constants import MESSAGE_NOT_VALID_FIELDS
from src.utils.constants import MESSAGE_NOT_EXISTS_USER
from src.utils.constants import MESSAGE_NOT_VALID_PASSWORD


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def login() -> Response:
    form = request.get_json()

    user_repository = UserRepository()

    username = form.get("username", "").strip()
    password = form.get("password", "").strip()

    if not username or not password:
        flash(MESSAGE_NOT_VALID_FIELDS, FLASH_ERROR)

        response = {
            "message": MESSAGE_NOT_VALID_FIELDS,
            "code": CODE_NOT_VALID_FIELDS,
            "redirect_to": current_app.config["LOGIN_VIEW_PATH"]
        }
        status_code = 400
        
        return make_response(response, status_code)

    user_exists = user_repository.get_user_by_username(username=username)

    if not user_exists:
        flash(MESSAGE_NOT_EXISTS_USER, FLASH_ERROR)

        response = {
            "message": MESSAGE_NOT_EXISTS_USER,
            "code": CODE_NOT_EXISTS_USER,
            "redirect_to": current_app.config["LOGIN_VIEW_PATH"]
        }
        status_code = 404
        
        return make_response(response, status_code)
    
    if not check_password_hash(user_exists.password, password):
        flash(MESSAGE_NOT_VALID_PASSWORD, FLASH_ERROR)

        response = {
            "message": MESSAGE_NOT_VALID_PASSWORD,
            "code": CODE_NOT_VALID_PASSWORD,
            "redirect_to": current_app.config["LOGIN_VIEW_PATH"]
        }
        status_code = 400
        
        return make_response(response, status_code)

    user = user_exists
    
    login_user(user=user, remember=True)

    flash("You have successfully logged in.", FLASH_SUCCESS)
    
    response = {
        "message": MESSAGE_SUCCESFULLY_LOGGED_IN,
        "code": CODE_SUCCESFULLY_LOGGED_IN,
        "redirect_to": current_app.config["HOME_VIEW_PATH"]
    }
    status_code = 200
    
    return make_response(response, status_code)


def logout() -> Response:
    logout_user()

    flash(MESSAGE_SUCCESFULLY_LOGOUT, FLASH_SUCCESS)

    response = {
        "message": MESSAGE_SUCCESFULLY_LOGOUT,
        "code": CODE_SUCCESFULLY_LOGOUT,
        "redirect_to": current_app.config["LOGIN_VIEW_PATH"]
    }
    status_code = 200
    
    return make_response(response, status_code)


def sign_up() -> Response:
    form = request.get_json()
    user_repository = UserRepository()

    username = form.get("username", "").strip()
    password = form.get("password", "").strip()
    email = form.get("email", "").strip()
    
    if not username or not password or not email:
        flash(MESSAGE_NOT_VALID_FIELDS, FLASH_ERROR)

        response = {
            "message": MESSAGE_NOT_VALID_FIELDS,
            "code": CODE_NOT_VALID_FIELDS,
            "redirect_to": current_app.config["SIGN_UP_VIEW_PATH"]
        }
        status_code = 400
        
        return make_response(response, status_code)
    
    username_exists = user_repository.get_user_by_username(username=username)
    email_exists = user_repository.get_user_by_email(email=email)

    if email_exists or username_exists:
        flash(MESSAGE_ALREADY_USER_EXISTS, FLASH_ERROR)

        response = {
            "message": MESSAGE_ALREADY_USER_EXISTS,
            "code": CODE_ALREADY_USER_EXISTS,
            "redirect_to": current_app.config["SIGN_UP_VIEW_PATH"]
        }
        status_code = 400
        
        return make_response(response, status_code)
    
    user_repository.add_user(username=username, email=email, password=password)

    flash(MESSAGE_SUCCESFULLY_SIGN_UP, FLASH_SUCCESS)

    response = {
        "message": MESSAGE_SUCCESFULLY_SIGN_UP,
        "code": CODE_SUCCESFULLY_SIGN_UP,
        "redirect_to": current_app.config["LOGIN_VIEW_PATH"]
    }
    status_code = 201
    
    return make_response(response, status_code)