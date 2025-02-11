import logging

from flask import Response
from flask import request
from flask import current_app
from flask import flash
from flask import redirect
from flask import url_for
from flask_login import login_user
from flask_login import logout_user
from werkzeug.security import check_password_hash

from src.data_access.user_repository import UserRepository


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def login() -> Response:
    form = request.form
    user_repository = UserRepository()

    username = form.get("username", "").strip()
    password = form.get("password", "").strip()

    if not username or not password:
        flash("You must enter valid fields to login.", "error")
        return redirect(url_for(current_app.config["LOGIN_VIEW"]))

    user_exists = user_repository.get_user_by_username(username=username)

    if not user_exists:
        flash("There is no account with the entered username.", "error")
        return redirect(url_for(current_app.config["LOGIN_VIEW"]))
    
    if not check_password_hash(user_exists.password, password):
        flash("The password entered is not valid.", "error")
        return redirect(url_for(current_app.config["LOGIN_VIEW"]))

    user = user_exists
    
    login_user(user=user, remember=True)

    flash("You have successfully logged in.", "success")
    return redirect(url_for(current_app.config["HOME_VIEW"]))


def logout() -> Response:
    logout_user()

    flash("You have successfully disconnected.", "success")
    return redirect(url_for(current_app.config["LOGIN_VIEW"]))


def sign_up() -> Response:
    form = request.form
    user_repository = UserRepository()

    username = form.get("username", "").strip()
    password = form.get("password", "").strip()
    email = form.get("email", "").strip()
    
    if not username or not password or not email:
        flash("You must enter valid fields to register.", "error")
        return redirect(url_for(current_app.config["SIGN_UP_VIEW"]))
    
    username_exists = user_repository.get_user_by_username(username=username)
    email_exists = user_repository.get_user_by_email(email=email)

    if email_exists or username_exists:
        flash("The entered email or username already exists.", "error")
        return redirect(url_for(current_app.config["SIGN_UP_VIEW"]))
    
    user_repository.add_user(username=username, email=email, password=password)

    flash("Your account was successfully created.", "success")
    return redirect(url_for(current_app.config["LOGIN_VIEW"]))