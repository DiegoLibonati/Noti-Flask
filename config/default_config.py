import os

# from src.constants.paths import ROOT_PATH
from src.constants.vars import (
    APP_VIEW_ROUTE_NAME,
    AUTH_BLUEPRINT_ROUTE_NAME,
    AUTH_VIEW_ROUTE_NAME,
    BLUEPRINT_AUTH_PATH,
    BLUEPRINT_NOTES_PATH,
    NOTES_BLUEPRINT_ROUTE_NAME,
    VIEW_APP_PATH,
    VIEW_AUTH_PATH,
)


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))

    # Without Docker use this keys
    # SQL_DB_NAME = os.getenv("SQL_DB_NAME") if os.getenv("SQL_DB_NAME").endswith('.db') else f'{os.getenv("SQL_DB_NAME")}.db'
    # DB_PATH = os.path.join(ROOT_PATH, SQL_DB_NAME)
    # SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"

    # With Docker use this keys
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_PORT = os.getenv("MYSQL_PORT", 3306)
    MYSQL_SERVICE = os.getenv("MYSQL_SERVICE")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVICE}:{MYSQL_PORT}/{MYSQL_DATABASE}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOGIN_ROUTE = f"{AUTH_BLUEPRINT_ROUTE_NAME}.login"
    LOGOUT_ROUTE = f"{AUTH_BLUEPRINT_ROUTE_NAME}.logout"
    SIGN_UP_ROUTE = f"{AUTH_BLUEPRINT_ROUTE_NAME}.sign_up"
    CREATE_NOTE_ROUTE = f"{NOTES_BLUEPRINT_ROUTE_NAME}.create"
    DELETE_NOTE_ROUTE = f"{NOTES_BLUEPRINT_ROUTE_NAME}.delete"
    EDIT_NOTE_ROUTE = f"{NOTES_BLUEPRINT_ROUTE_NAME}.edit"

    LOGIN_ROUTE_PATH = f"{BLUEPRINT_AUTH_PATH}/login"
    LOGOUT_ROUTE_PATH = f"{BLUEPRINT_AUTH_PATH}/logout"
    SIGN_UP_ROUTE_PATH = f"{BLUEPRINT_AUTH_PATH}/sign_up"
    CREATE_NOTE_ROUTE_PATH = f"{BLUEPRINT_NOTES_PATH}/create"
    DELETE_NOTE_ROUTE_PATH = f"{BLUEPRINT_NOTES_PATH}/delete"
    EDIT_NOTE_ROUTE_PATH = f"{BLUEPRINT_NOTES_PATH}/edit"

    LOGIN_VIEW = f"{AUTH_VIEW_ROUTE_NAME}.login"
    SIGN_UP_VIEW = f"{AUTH_VIEW_ROUTE_NAME}.sign_up"
    HOME_VIEW = f"{APP_VIEW_ROUTE_NAME}.home"

    LOGIN_VIEW_PATH = f"{VIEW_AUTH_PATH}/login"
    SIGN_UP_VIEW_PATH = f"{VIEW_AUTH_PATH}/sign_up"
    HOME_VIEW_PATH = f"{VIEW_APP_PATH}/home"

    DEBUG = False
    TESTING = False
