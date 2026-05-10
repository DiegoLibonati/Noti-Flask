from collections.abc import Generator

import pytest
from flask import Flask
from sqlalchemy.pool import StaticPool

from src import create_app
from src.configs.sql_alchemy_config import db
from src.models.orm.user import User
from src.services.encrypt_service import EncryptService


@pytest.fixture(scope="session")
def app() -> Generator[Flask, None, None]:
    flask_app: Flask = create_app("testing")
    flask_app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }
    with flask_app.app_context():
        db.create_all()
    yield flask_app
    with flask_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app: Flask):
    return app.test_client()


@pytest.fixture(scope="function")
def db_session(app: Flask) -> Generator[None, None, None]:
    with app.app_context():
        yield
        db.session.rollback()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()


@pytest.fixture(scope="function")
def auth_client(app: Flask, client, db_session: None):
    with app.app_context():
        user: User = User(
            username="testuser",
            email="test@test.com",
            password=EncryptService("testpass123").password_hashed,
        )
        db.session.add(user)
        db.session.commit()
        user_id: int = user.id

    with client.session_transaction() as sess:
        sess["_user_id"] = str(user_id)
        sess["_fresh"] = True

    return client
