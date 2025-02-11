from flask import Flask

from src.utils.utils import get_extra_files_paths
from src.utils.utils import get_extra_files
from src.utils.utils import get_context_by_key


def test_get_extra_files_paths(flask_app: Flask) -> None:
    extra_files_paths = get_extra_files_paths(app=flask_app)

    assert extra_files_paths

    for extra_file_path in extra_files_paths:
        assert extra_file_path


def test_get_extra_files(flask_app: Flask) -> None:
    extra_files = get_extra_files(app=flask_app)

    assert extra_files

    for extra_file in extra_files:
        assert extra_file


def test_get_context_by_key(flask_app: Flask) -> None:
    context = get_context_by_key(app=flask_app, key="login")

    assert context
    assert context.get("sign_up_view")
    assert context.get("login_route")