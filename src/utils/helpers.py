import glob
from typing import Any

from flask import Flask

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


def get_watch_patterns() -> list[str]:
    return [
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


def get_extra_files() -> list[str]:
    extra_files = []
    for pattern in get_watch_patterns():
        extra_files.extend(glob.glob(pattern, recursive=True))
    return extra_files


def get_context_by_key(app: Flask, key: str, **extra: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "login": {
            "sign_up_view": app.config["SIGN_UP_VIEW"],
            "login_route": app.config["LOGIN_ROUTE"],
        },
        "register": {
            "login_view": app.config["LOGIN_VIEW"],
            "sign_up_route": app.config["SIGN_UP_ROUTE"],
        },
        "home": {
            "current_route": "Home",
            "logout_route": app.config["LOGOUT_ROUTE"],
        },
    }.get(key, {})

    return {**base, **extra}
