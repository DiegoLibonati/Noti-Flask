import importlib
import os

import sass
from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from flask_migrate import Migrate, upgrade
from flask_scss import Scss

from config.logger_config import setup_logger
from config.sql_alchemy_config import db
from src.blueprints.routes import register_routes
from src.constants.paths import CSS_FOLDER_PATH, SCSS_FOLDER_PATH
from src.models.orm.user import User
from src.services.user_service import UserService
from src.views.routes import register_views

logger = setup_logger()


def create_app(config_name="development"):
    app = Flask(__name__)

    output_style = "compressed"

    config_module = importlib.import_module(f"config.{config_name}_config")
    app.config.from_object(config_module.__dict__[f"{config_name.capitalize()}Config"])

    if config_name.lower() == "development":
        sass.compile(
            dirname=(SCSS_FOLDER_PATH, CSS_FOLDER_PATH), output_style=output_style
        )

    Scss(app=app, static_dir=CSS_FOLDER_PATH, asset_dir=SCSS_FOLDER_PATH)

    db.init_app(app)
    Migrate(app, db)

    if config_name.lower() != "testing":
        with app.app_context():
            if config_name.lower() == "development" and app.config[
                "SQLALCHEMY_DATABASE_URI"
            ].startswith("sqlite"):
                db_path = app.config["DB_PATH"]
                if not os.path.exists(db_path):
                    db.create_all()
                    logger.info("SQLite DB Created")

            if config_name.lower() == "development":
                upgrade()

    login_manager = LoginManager()
    login_manager.login_view = app.config["LOGIN_VIEW"]
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id: str) -> User:
        return UserService.get_user_by_id(id=int(id))

    register_routes(app)

    register_views(app)

    @app.errorhandler(404)
    def page_not_found(_):
        if not current_user.is_authenticated:
            return redirect(url_for(app.config["LOGIN_VIEW"]))

        return redirect(url_for(app.config["HOME_VIEW"]))

    app.jinja_env.add_extension("jinja2.ext.loopcontrols")

    return app
