import os

import sass
from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_scss import Scss

from src.extensions import db
from src.models.db.User import User
from src.data_access.user_repository import UserRepository
from src.views.v1.auth.auth_views import auth_views
from src.views.v1.app.app_views import app_views
from src.blueprints.v1.auth_route import auth_route
from src.blueprints.v1.notes_route import notes_route
from src.utils.constants import STATIC_FOLDER_NAME
from src.utils.constants import CSS_FOLDER_NAME
from src.utils.constants import SCSS_FOLDER_NAME
from src.utils.constants import GENERAL_TEMPLATES_FOLDER_NAME
from src.utils.constants import AUTH_TEMPLATES_FOLDER_NAME
from src.utils.constants import APP_TEMPLATES_FOLDER_NAME
from src.utils.constants import GENERAL_VIEWS_FOLDER_NAME
from src.utils.constants import AUTH_VIEWS_FOLDER_NAME
from src.utils.constants import APP_VIEWS_FOLDER_NAME
from src.utils.constants import VERSION_VIEWS
from src.utils.constants import AUTH_BLUEPRINT_ROUTE_NAME
from src.utils.constants import NOTES_BLUEPRINT_ROUTE_NAME
from src.utils.constants import AUTH_VIEW_ROUTE_NAME
from src.utils.constants import APP_VIEW_ROUTE_NAME
from src.utils.constants import BLUEPRINT_AUTH_PATH
from src.utils.constants import BLUEPRINT_NOTES_PATH
from src.utils.constants import VIEW_AUTH_PATH
from src.utils.constants import VIEW_APP_PATH


# Vars
ROOT_FILE_PATH = os.path.dirname(__file__)


def setup_config(app: Flask) -> None:
    load_dotenv()

    # App Config Globals
    app.config["TESTING"] = False

    # App Config With App Envs
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQL_DB_NAME"] = os.getenv("SQL_DB_NAME") if os.getenv("SQL_DB_NAME").endswith('.db') else f'{os.getenv("SQL_DB_NAME")}.db'
    app.config["HOST"] = os.getenv("HOST", "0.0.0.0")
    app.config["PORT"] = int(os.getenv("PORT", 5000)) 

    # App Config With Flask Envs
    app.config["FLASK_DEBUG"] = os.getenv("FLASK_DEBUG")
    app.config["FLASK_ENV"] = os.getenv("FLASK_ENV")

    # App Config Paths
    app.config["DB_PATH"] = os.path.join(ROOT_FILE_PATH, app.config['SQL_DB_NAME'])
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.config['DB_PATH']}"
    app.config["CSS_FOLDER_PATH"] = os.path.join(ROOT_FILE_PATH, STATIC_FOLDER_NAME, CSS_FOLDER_NAME)
    app.config["SCSS_FOLDER_PATH"] = os.path.join(ROOT_FILE_PATH, STATIC_FOLDER_NAME, SCSS_FOLDER_NAME)
    app.config["GENERAL_TEMPLATES_FOLDER_PATH"] = os.path.join(ROOT_FILE_PATH, GENERAL_TEMPLATES_FOLDER_NAME)
    app.config["APP_TEMPLATES_FOLDER_PATH"] = os.path.join(ROOT_FILE_PATH, GENERAL_VIEWS_FOLDER_NAME, VERSION_VIEWS, APP_VIEWS_FOLDER_NAME,  APP_TEMPLATES_FOLDER_NAME)
    app.config["AUTH_TEMPLATES_FOLDER_PATH"] = os.path.join(ROOT_FILE_PATH, GENERAL_VIEWS_FOLDER_NAME, VERSION_VIEWS, AUTH_VIEWS_FOLDER_NAME,  AUTH_TEMPLATES_FOLDER_NAME)

    # App Config Template Names
    app.config["TEMPLATE_LOGIN_NAME"] = "login.html"
    app.config["TEMPLATE_SIGN_UP_NAME"] = "sign_up.html"
    app.config["TEMPLATE_HOME_NAME"] = "home.html"

    # Blueprints
    app.config["LOGIN_ROUTE"] = f"{AUTH_BLUEPRINT_ROUTE_NAME}.login"
    app.config["LOGIN_ROUTE_PATH"] = f"{BLUEPRINT_AUTH_PATH}/login"

    app.config["LOGOUT_ROUTE"] = f"{AUTH_BLUEPRINT_ROUTE_NAME}.logout"
    app.config["LOGOUT_ROUTE_PATH"] = f"{BLUEPRINT_AUTH_PATH}/logout"

    app.config["SIGN_UP_ROUTE"] = f"{AUTH_BLUEPRINT_ROUTE_NAME}.sign_up"
    app.config["SIGN_UP_ROUTE_PATH"] = f"{BLUEPRINT_AUTH_PATH}/sign_up"

    app.config["CREATE_NOTE_ROUTE"] = f"{NOTES_BLUEPRINT_ROUTE_NAME}.create"
    app.config["CREATE_NOTE_ROUTE_PATH"] = f"{BLUEPRINT_NOTES_PATH}/create"

    app.config["DELETE_NOTE_ROUTE"] = f"{NOTES_BLUEPRINT_ROUTE_NAME}.delete"
    app.config["DELETE_NOTE_ROUTE_PATH"] = f"{BLUEPRINT_NOTES_PATH}/delete"

    app.config["EDIT_NOTE_ROUTE"] = f"{NOTES_BLUEPRINT_ROUTE_NAME}.edit"
    app.config["EDIT_NOTE_ROUTE_PATH"] = f"{BLUEPRINT_NOTES_PATH}/edit"
    
    # Views
    app.config["LOGIN_VIEW"] = f"{AUTH_VIEW_ROUTE_NAME}.login"
    app.config["LOGIN_VIEW_PATH"] = f"{VIEW_AUTH_PATH}/login"

    app.config["SIGN_UP_VIEW"] = f"{AUTH_VIEW_ROUTE_NAME}.sign_up"
    app.config["SIGN_UP_VIEW_PATH"] = f"{VIEW_AUTH_PATH}/sign_up"
    
    app.config["HOME_VIEW"] = f"{APP_VIEW_ROUTE_NAME}.home"
    app.config["HOME_VIEW_PATH"] = f"{VIEW_APP_PATH}/home"

    # Jinja Config
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

    print(f"APP Config: {app.config}")


def setup_scss(app: Flask) -> None:
    dir_scss_folder = app.config["SCSS_FOLDER_PATH"]
    dir_css_folder = app.config["CSS_FOLDER_PATH"]

    output_style="compressed"

    sass.compile(dirname=(dir_scss_folder, dir_css_folder), output_style=output_style)

    Scss(app=app, static_dir=dir_css_folder, asset_dir=dir_scss_folder)


def setup_db(app: Flask) -> None:
    db.init_app(app=app)
    Migrate(app=app, db=db)


def create_db(app: Flask) -> None:
    db_path = app.config["DB_PATH"]

    if os.path.exists(db_path):
        print("DB EXISTS!")
        return
    
    with app.app_context():
        db.create_all()
        print("DB Created")


def setup_login(app: Flask) -> None:
    login_manager = LoginManager()
    login_manager.login_view = app.config["LOGIN_VIEW"]
    login_manager.init_app(app=app)

    @login_manager.user_loader
    def load_user(id: str) -> User:
        user_repository = UserRepository()
        return user_repository.get_user_by_id(id=int(id))


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(auth_route, url_prefix=BLUEPRINT_AUTH_PATH)
    app.register_blueprint(notes_route, url_prefix=BLUEPRINT_NOTES_PATH)


def register_views(app: Flask) -> None:
    app.register_blueprint(auth_views, url_prefix=VIEW_AUTH_PATH)
    app.register_blueprint(app_views, url_prefix=VIEW_APP_PATH)


def create_app():
    app = Flask(__name__)

    # Load Config
    setup_config(app=app)

    # Load CSS / SCSS
    setup_scss(app=app)

    # Load DB
    setup_db(app=app)
    
    # Create DB
    create_db(app=app)

    # Login Manager
    setup_login(app=app)

    # Load Routes
    register_blueprints(app=app)

    # Load Views
    register_views(app=app)

    return app