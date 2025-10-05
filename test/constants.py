import os

from src.constants.vars import (
    BLUEPRINT_AUTH_PATH,
    BLUEPRINT_NOTES_PATH,
    VIEW_APP_PATH,
    VIEW_AUTH_PATH,
)

BLUEPRINTS = {
    "auth": BLUEPRINT_AUTH_PATH,
    "notes": BLUEPRINT_NOTES_PATH,
}

VIEWS = {"app_views": VIEW_APP_PATH, "auth_views": VIEW_AUTH_PATH}

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
COMPOSE_FILE = os.path.join(PROJECT_ROOT, "dev.docker-compose.yml")
