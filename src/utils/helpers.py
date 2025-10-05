import glob
from typing import Any

from flask import Flask
from flask_login import current_user

from src.constants.paths import (
    APP_FILES_PATH,
    APP_FILES_PATH_2,
    AUTH_FILES_PATH,
    AUTH_FILES_PATH_2,
    GENERAL_FILES_PATH,
    GENERAL_FILES_PATH_2,
    JS_FILES_PATH,
    JS_FILES_PATH_2,
    SCCS_FILES_PATH,
    SCCS_FILES_PATH_2,
)


def get_extra_files_paths() -> list[str]:
    extra_files_paths = [
        SCCS_FILES_PATH,
        SCCS_FILES_PATH_2,
        GENERAL_FILES_PATH,
        GENERAL_FILES_PATH_2,
        APP_FILES_PATH,
        APP_FILES_PATH_2,
        AUTH_FILES_PATH,
        AUTH_FILES_PATH_2,
        JS_FILES_PATH,
        JS_FILES_PATH_2,
    ]

    return extra_files_paths


def get_extra_files() -> list[str]:
    extra_files = []
    extra_files_paths = get_extra_files_paths()

    for extra_files_path in extra_files_paths:
        extra_files.extend(glob.glob(extra_files_path, recursive=True))

    return extra_files


def get_context_by_key(app: Flask, key: str) -> dict[str, Any]:
    return {
        "login": {
            "sign_up_view": app.config["SIGN_UP_VIEW"],
            "login_route": app.config["LOGIN_ROUTE"],
            "user": current_user,
        },
        "register": {
            "login_view": app.config["LOGIN_VIEW"],
            "sign_up_route": app.config["SIGN_UP_ROUTE"],
            "user": current_user,
        },
        "home": {
            "current_route": "Home",
            "logout_route": app.config["LOGOUT_ROUTE"],
            "user": current_user,
        },
    }.get(key)
