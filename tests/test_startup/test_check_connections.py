from unittest.mock import MagicMock, call, patch

import pytest
from flask import Flask
from sqlalchemy.exc import OperationalError

from src.startup.check_connections import (
    CONNECT_TIMEOUT_SECONDS,
    MAX_CONNECTION_ATTEMPTS,
    MYSQL_SERVICE_NAME,
    RETRY_DELAY_SECONDS,
    check_connections,
    check_mysql_connection,
)


def build_app(check_connections_enabled: bool = True, mysql_host: str | None = "localhost") -> Flask:
    app: Flask = Flask(__name__)
    app.config["CHECK_CONNECTIONS"] = check_connections_enabled
    app.config["MYSQL_HOST"] = mysql_host
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://user:pass@localhost:3306/db"
    return app


def build_connection_error() -> OperationalError:
    return OperationalError("SELECT 1", None, Exception("connection refused"))


class TestCheckMysqlConnection:
    @pytest.mark.unit
    def test_success_on_first_attempt_does_not_warn_or_retry(self) -> None:
        app: Flask = build_app()
        with (
            patch("src.startup.check_connections.create_engine") as mock_create_engine,
            patch("src.startup.check_connections.time.sleep") as mock_sleep,
            patch("src.startup.check_connections.logger") as mock_logger,
        ):
            check_mysql_connection(app)
        mock_create_engine.assert_called_once_with(
            app.config["SQLALCHEMY_DATABASE_URI"],
            connect_args={"connect_timeout": CONNECT_TIMEOUT_SECONDS},
        )
        mock_logger.info.assert_called_once()
        mock_logger.warning.assert_not_called()
        mock_sleep.assert_not_called()
        mock_create_engine.return_value.dispose.assert_called_once()

    @pytest.mark.unit
    def test_success_on_third_attempt_warns_twice_then_stops_retrying(self) -> None:
        app: Flask = build_app()
        mock_engine: MagicMock = MagicMock()
        mock_engine.connect.side_effect = [build_connection_error(), build_connection_error(), MagicMock()]
        with (
            patch("src.startup.check_connections.create_engine", return_value=mock_engine),
            patch("src.startup.check_connections.time.sleep") as mock_sleep,
            patch("src.startup.check_connections.logger") as mock_logger,
        ):
            check_mysql_connection(app)
        assert mock_logger.warning.call_count == 2
        mock_logger.info.assert_called_once()
        assert mock_engine.connect.call_count == 3
        assert mock_sleep.call_args_list == [call(RETRY_DELAY_SECONDS), call(RETRY_DELAY_SECONDS)]

    @pytest.mark.unit
    def test_all_attempts_fail_emits_final_warning_and_returns_normally(self) -> None:
        app: Flask = build_app()
        mock_engine: MagicMock = MagicMock()
        mock_engine.connect.side_effect = [build_connection_error() for _ in range(MAX_CONNECTION_ATTEMPTS)]
        with (
            patch("src.startup.check_connections.create_engine", return_value=mock_engine),
            patch("src.startup.check_connections.time.sleep") as mock_sleep,
            patch("src.startup.check_connections.logger") as mock_logger,
        ):
            check_mysql_connection(app)
        assert mock_engine.connect.call_count == MAX_CONNECTION_ATTEMPTS
        assert mock_sleep.call_count == MAX_CONNECTION_ATTEMPTS - 1
        assert mock_logger.warning.call_count == MAX_CONNECTION_ATTEMPTS + 1
        final_warning: str = mock_logger.warning.call_args[0][0]
        assert "The app will continue running" in final_warning
        mock_logger.info.assert_not_called()
        mock_engine.dispose.assert_called_once()

    @pytest.mark.unit
    def test_mysql_not_configured_skips_connection_attempt(self) -> None:
        app: Flask = build_app(mysql_host=None)
        with (
            patch("src.startup.check_connections.create_engine") as mock_create_engine,
            patch("src.startup.check_connections.logger") as mock_logger,
        ):
            check_mysql_connection(app)
        mock_create_engine.assert_not_called()
        mock_logger.info.assert_called_once()

    @pytest.mark.unit
    def test_service_name_is_mysql(self) -> None:
        assert MYSQL_SERVICE_NAME == "MySQL"


class TestCheckConnections:
    @pytest.mark.unit
    def test_disabled_flag_skips_all_checks(self) -> None:
        app: Flask = build_app(check_connections_enabled=False)
        with patch("src.startup.check_connections.check_mysql_connection") as mock_check:
            check_connections(app)
        mock_check.assert_not_called()

    @pytest.mark.unit
    def test_enabled_flag_runs_mysql_check(self) -> None:
        app: Flask = build_app()
        with patch("src.startup.check_connections.check_mysql_connection") as mock_check:
            check_connections(app)
        mock_check.assert_called_once_with(app)
