from test.constants import BLUEPRINTS
from typing import Any

from flask.testing import FlaskClient
from pytest import MonkeyPatch
from werkzeug.test import TestResponse

from src.constants.codes import (
    CODE_DELETE_NOTE,
    CODE_EDIT_NOTE,
    CODE_ERROR_DELETE_NOTE,
    CODE_ERROR_UPDATE_NOTE,
    CODE_NOT_EXISTS_NOTE,
    CODE_NOT_VALID_FIELDS,
    CODE_NOT_VALID_ID,
)
from src.services.note_service import NoteService


def test_alive(flask_client: FlaskClient) -> None:
    res: TestResponse = flask_client.get(f"{BLUEPRINTS['notes']}/alive")
    body: dict[str, Any] = res.get_json()

    assert res.status_code == 200
    assert body["name_bp"] == "Note"
    assert body["message"] == "I am Alive!"


def test_create_success(
    monkeypatch: MonkeyPatch,
    authenticated_client: FlaskClient,
    unique_note: dict[str, Any],
) -> None:
    def mock_add_note(note: dict[str, Any]) -> bool:
        return True

    monkeypatch.setattr(NoteService, "add_note", mock_add_note)

    res: TestResponse = authenticated_client.post(
        f"{BLUEPRINTS['notes']}/",
        data={"content": unique_note["content"]},
        follow_redirects=False,
    )

    assert res.status_code == 302
    assert "/home" in res.headers["Location"]


def test_delete_invalid_id(authenticated_client: FlaskClient) -> None:
    res: TestResponse = authenticated_client.delete(
        f"{BLUEPRINTS['notes']}/abc", follow_redirects=False
    )

    assert res.status_code == 400

    body = res.get_json()

    assert body["code"] == CODE_NOT_VALID_ID


def test_delete_not_exists(
    monkeypatch: MonkeyPatch, authenticated_client: FlaskClient
) -> None:
    monkeypatch.setattr(NoteService, "get_note_by_id", lambda id: None)

    res: TestResponse = authenticated_client.delete(
        f"{BLUEPRINTS['notes']}/1", follow_redirects=False
    )

    assert res.status_code == 404

    body = res.get_json()

    assert body["code"] == CODE_NOT_EXISTS_NOTE


def test_delete_error_on_service(
    monkeypatch: MonkeyPatch,
    authenticated_client: FlaskClient,
    unique_note: dict[str, Any],
) -> None:
    monkeypatch.setattr(NoteService, "get_note_by_id", lambda id: unique_note)
    monkeypatch.setattr(NoteService, "delete_note", lambda note: False)

    res: TestResponse = authenticated_client.delete(
        f"{BLUEPRINTS['notes']}/1", follow_redirects=False
    )

    assert res.status_code == 400

    body = res.get_json()

    assert body["code"] == CODE_ERROR_DELETE_NOTE


def test_delete_success(
    monkeypatch: MonkeyPatch,
    authenticated_client: FlaskClient,
    unique_note: dict[str, Any],
) -> None:
    monkeypatch.setattr(NoteService, "get_note_by_id", lambda id: unique_note)
    monkeypatch.setattr(NoteService, "delete_note", lambda note: True)

    res: TestResponse = authenticated_client.delete(
        f"{BLUEPRINTS['notes']}/1", follow_redirects=False
    )

    assert res.status_code == 200

    body = res.get_json()

    assert body["code"] == CODE_DELETE_NOTE


def test_edit_invalid_id(authenticated_client: FlaskClient) -> None:
    res: TestResponse = authenticated_client.patch(
        f"{BLUEPRINTS['notes']}/abc", json={}, follow_redirects=False
    )

    assert res.status_code == 400

    body = res.get_json()

    assert body["code"] == CODE_NOT_VALID_ID


def test_edit_missing_fields(authenticated_client: FlaskClient) -> None:
    res: TestResponse = authenticated_client.patch(
        f"{BLUEPRINTS['notes']}/1", json={}, follow_redirects=False
    )

    assert res.status_code == 400

    body = res.get_json()

    assert body["code"] == CODE_NOT_VALID_FIELDS


def test_edit_note_not_found(
    monkeypatch: MonkeyPatch, authenticated_client: FlaskClient
) -> None:
    monkeypatch.setattr(NoteService, "get_note_by_id", lambda id: None)

    res: TestResponse = authenticated_client.patch(
        f"{BLUEPRINTS['notes']}/1", json={"content": "updated"}, follow_redirects=False
    )

    assert res.status_code == 400

    body = res.get_json()

    assert body["code"] == CODE_ERROR_DELETE_NOTE


def test_edit_update_error(
    monkeypatch: MonkeyPatch,
    authenticated_client: FlaskClient,
    unique_note: dict[str, Any],
) -> None:
    monkeypatch.setattr(NoteService, "get_note_by_id", lambda id: unique_note)
    monkeypatch.setattr(NoteService, "update_note", lambda note, data: False)

    res: TestResponse = authenticated_client.patch(
        f"{BLUEPRINTS['notes']}/1", json={"content": "updated"}, follow_redirects=False
    )

    assert res.status_code == 400

    body = res.get_json()

    assert body["code"] == CODE_ERROR_UPDATE_NOTE


def test_edit_success(
    monkeypatch: MonkeyPatch,
    authenticated_client: FlaskClient,
    unique_note: dict[str, Any],
) -> None:
    monkeypatch.setattr(NoteService, "get_note_by_id", lambda id: unique_note)
    monkeypatch.setattr(NoteService, "update_note", lambda note, data: True)

    res: TestResponse = authenticated_client.patch(
        f"{BLUEPRINTS['notes']}/1", json={"content": "updated"}, follow_redirects=False
    )

    assert res.status_code == 200

    body = res.get_json()

    assert body["code"] == CODE_EDIT_NOTE
