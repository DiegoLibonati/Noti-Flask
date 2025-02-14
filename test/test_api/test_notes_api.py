from typing import Any

from flask import Flask
from flask import Response
from flask.testing import FlaskClient

from src.data_access.note_repository import NoteRepository
from src.utils.constants import FLASH_SUCCESS
from src.utils.constants import FLASH_ERROR
from src.utils.constants import CODE_CREATE_NOTE
from src.utils.constants import CODE_DELETE_NOTE
from src.utils.constants import CODE_NOT_EXISTS_NOTE
from src.utils.constants import MESSAGE_CREATE_NOTE
from src.utils.constants import MESSAGE_DELETE_NOTE
from src.utils.constants import MESSAGE_NOT_EXISTS_NOTE


def test_create_note(authenticated_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], note_repository: NoteRepository) -> None:
    response: Response = authenticated_client.post(
        f"{blueprints['notes']}/create"
    )

    status_code = response.status_code
    data = response.get_json()

    assert status_code == 201
    assert data.get("message") == MESSAGE_CREATE_NOTE
    assert data.get("code") == CODE_CREATE_NOTE
    assert data.get("redirect_to") == flask_app.config["HOME_VIEW_PATH"]

    with authenticated_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert (FLASH_SUCCESS, MESSAGE_CREATE_NOTE) in flashes

    notes = note_repository.get_notes()
    last_note = notes[len(notes) - 1]

    assert last_note


def test_delete_note_invalid_id(authenticated_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any]) -> None:
    id = "99999999"

    response: Response = authenticated_client.delete(
        f"{blueprints['notes']}/delete/{id}"
    )

    status_code = response.status_code
    data = response.get_json()

    assert status_code == 404
    assert data.get("message") == MESSAGE_NOT_EXISTS_NOTE
    assert data.get("code") == CODE_NOT_EXISTS_NOTE
    assert data.get("redirect_to") == flask_app.config["HOME_VIEW_PATH"]

    with authenticated_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert (FLASH_ERROR, MESSAGE_NOT_EXISTS_NOTE) in flashes


def test_delete_note(authenticated_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], note_repository: NoteRepository) -> None:
    notes = note_repository.get_notes()
    last_note = notes[len(notes) - 1]

    assert last_note

    response: Response = authenticated_client.delete(
        f"{blueprints['notes']}/delete/{last_note.id}"
    )

    status_code = response.status_code
    data = response.get_json()

    assert status_code == 200
    assert data.get("message") == MESSAGE_DELETE_NOTE
    assert data.get("code") == CODE_DELETE_NOTE
    assert data.get("redirect_to") == flask_app.config["HOME_VIEW_PATH"]

    with authenticated_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert (FLASH_SUCCESS, MESSAGE_DELETE_NOTE) in flashes