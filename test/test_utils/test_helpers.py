from unittest.mock import patch

from pytest import MonkeyPatch

from src.constants.paths import (
    APP_FILES_PATH,
    APP_FILES_PATH_2,
    AUTH_FILES_PATH,
    AUTH_FILES_PATH_2,
    GENERAL_FILES_PATH,
    GENERAL_FILES_PATH_2,
    SCCS_FILES_PATH,
    SCCS_FILES_PATH_2,
)
from src.utils.helpers import get_extra_files, get_extra_files_paths


def test_get_extra_files_paths() -> None:
    result: list[str] = get_extra_files_paths()

    expected_paths: list[str] = [
        SCCS_FILES_PATH,
        SCCS_FILES_PATH_2,
        GENERAL_FILES_PATH,
        GENERAL_FILES_PATH_2,
        APP_FILES_PATH,
        APP_FILES_PATH_2,
        AUTH_FILES_PATH,
        AUTH_FILES_PATH_2,
    ]

    assert isinstance(result, list)
    assert all(isinstance(p, str) for p in result)
    assert result == expected_paths
    assert len(result) == 8


def test_get_extra_files(monkeypatch: MonkeyPatch) -> None:
    mock_files: list[str] = ["file1.scss", "file2.html"]

    def fake_glob(path: str, recursive: bool = True) -> list[str]:
        return mock_files if "scss" in path or "html" in path else []

    with patch("src.utils.helpers.glob.glob", side_effect=fake_glob):
        result: list[str] = get_extra_files()

    assert isinstance(result, list)
    assert "file1.scss" in result
    assert "file2.html" in result
    assert all(isinstance(f, str) for f in result)
