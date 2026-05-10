import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.configs.sql_alchemy_config import db


class TestSQLAlchemyConfig:
    @pytest.mark.unit
    def test_db_is_sqlalchemy_instance(self) -> None:
        assert isinstance(db, SQLAlchemy)

    @pytest.mark.unit
    def test_db_is_initialized_with_app(self, app: Flask) -> None:
        assert app.extensions.get("sqlalchemy") is not None

    @pytest.mark.unit
    def test_db_session_available_within_app_context(self, app: Flask) -> None:
        with app.app_context():
            assert db.session is not None

    @pytest.mark.unit
    def test_db_metadata_has_tables_after_create_all(self, app: Flask) -> None:
        with app.app_context():
            table_names: list[str] = list(db.metadata.tables.keys())
            assert "notes" in table_names
            assert "users" in table_names
