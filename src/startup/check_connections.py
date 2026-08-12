import time

from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from src.configs.logger_config import setup_logger

logger = setup_logger(__name__)

MYSQL_SERVICE_NAME = "MySQL"
MAX_CONNECTION_ATTEMPTS = 5
RETRY_DELAY_SECONDS = 2
CONNECT_TIMEOUT_SECONDS = 3


def check_mysql_connection(app: Flask) -> None:
    if not app.config.get("MYSQL_HOST"):
        logger.info("%s is not configured. Skipping its connection check.", MYSQL_SERVICE_NAME)
        return

    engine = create_engine(
        app.config["SQLALCHEMY_DATABASE_URI"],
        connect_args={"connect_timeout": CONNECT_TIMEOUT_SECONDS},
    )

    try:
        for attempt in range(1, MAX_CONNECTION_ATTEMPTS + 1):
            try:
                with engine.connect() as connection:
                    connection.execute(text("SELECT 1"))
                logger.info(
                    "Connected to %s successfully (attempt %d/%d).",
                    MYSQL_SERVICE_NAME,
                    attempt,
                    MAX_CONNECTION_ATTEMPTS,
                )
                return
            except SQLAlchemyError as error:
                logger.warning(
                    "Could not connect to %s (attempt %d/%d): %s",
                    MYSQL_SERVICE_NAME,
                    attempt,
                    MAX_CONNECTION_ATTEMPTS,
                    error,
                )
                if attempt < MAX_CONNECTION_ATTEMPTS:
                    time.sleep(RETRY_DELAY_SECONDS)

        logger.warning(
            "Could not connect to %s after %d attempts. The app will continue running, "
            "but %s-dependent features will fail until the connection is available.",
            MYSQL_SERVICE_NAME,
            MAX_CONNECTION_ATTEMPTS,
            MYSQL_SERVICE_NAME,
        )
    finally:
        engine.dispose()


def check_connections(app: Flask) -> None:
    if not app.config.get("CHECK_CONNECTIONS"):
        return

    check_mysql_connection(app)
