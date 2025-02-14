import os
import glob
from typing import Any

from flask import Flask
from flask_login import current_user


def get_extra_files_paths(app: Flask) -> list[str]:
    extra_files_paths = [
        os.path.join(app.config["SCSS_FOLDER_PATH"], "*.scss"),
        os.path.join(app.config["SCSS_FOLDER_PATH"], "**", "*", "*.scss"),

        os.path.join(app.config["GENERAL_TEMPLATES_FOLDER_PATH"], "*.html"),
        os.path.join(app.config["GENERAL_TEMPLATES_FOLDER_PATH"], "**", "*", "*.html"),

        os.path.join(app.config["APP_TEMPLATES_FOLDER_PATH"], "*.html"),
        os.path.join(app.config["APP_TEMPLATES_FOLDER_PATH"], "**", "*", "*.html"),

        os.path.join(app.config["AUTH_TEMPLATES_FOLDER_PATH"], "*.html"),
        os.path.join(app.config["AUTH_TEMPLATES_FOLDER_PATH"], "**", "*", "*.html"),
    ]

    return extra_files_paths


def get_extra_files(app: Flask) -> list[str]:
    extra_files = []
    extra_files_paths = get_extra_files_paths(app=app)

    for extra_files_path in extra_files_paths:
        extra_files.extend(glob.glob(extra_files_path, recursive=True))

    return extra_files


def get_context_by_key(app: Flask, key: str) -> dict[str, Any]:
    return {
        "login": {
            "sign_up_view": app.config["SIGN_UP_VIEW"],
            "user": current_user,
        },
        "register": {
            "login_view": app.config["LOGIN_VIEW"],
            "user": current_user,
        },
        "home": {
            "current_route": "Home",
            "user": current_user,
        }
    }.get(key)