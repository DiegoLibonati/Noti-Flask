from typing import Any

from flask import Flask
from flask import Response
from flask.testing import FlaskClient

from src.data_access.note_repository import NoteRepository
from src.utils.constants import FLASH_SUCCESS
from src.utils.constants import FLASH_ERROR
from src.utils.constants import CODE_CREATE_NOTE
from src.utils.constants import CODE_DELETE_NOTE
from src.utils.constants import CODE_EDIT_NOTE
from src.utils.constants import CODE_NOT_EXISTS_NOTE
from src.utils.constants import CODE_NOT_VALID_FIELDS
from src.utils.constants import CODE_NOT_VALID_ID
from src.utils.constants import MESSAGE_CREATE_NOTE
from src.utils.constants import MESSAGE_DELETE_NOTE
from src.utils.constants import MESSAGE_EDIT_NOTE
from src.utils.constants import MESSAGE_NOT_EXISTS_NOTE
from src.utils.constants import MESSAGE_NOT_VALID_FIELDS
from src.utils.constants import MESSAGE_NOT_VALID_ID


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


def test_edit_note_invalid_id(authenticated_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any]) -> None:
    id = "asd"

    response: Response = authenticated_client.put(
        f"{blueprints['notes']}/edit/{id}"
    )

    status_code = response.status_code
    data = response.get_json()

    assert status_code == 400
    assert data.get("message") == MESSAGE_NOT_VALID_ID
    assert data.get("code") == CODE_NOT_VALID_ID
    assert data.get("redirect_to") == flask_app.config["HOME_VIEW_PATH"]

    with authenticated_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert (FLASH_ERROR, MESSAGE_NOT_VALID_ID) in flashes


def test_edit_note_invalid_fields(authenticated_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], note_repository: NoteRepository) -> None:
    notes = note_repository.get_notes()
    last_note = notes[len(notes) - 1]

    assert last_note

    response: Response = authenticated_client.put(
        f"{blueprints['notes']}/edit/{last_note.id}",
        json={
            "content": ""
        }
    )

    status_code = response.status_code
    data = response.get_json()

    assert status_code == 400
    assert data.get("message") == MESSAGE_NOT_VALID_FIELDS
    assert data.get("code") == CODE_NOT_VALID_FIELDS
    assert data.get("redirect_to") == flask_app.config["HOME_VIEW_PATH"]

    with authenticated_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert (FLASH_ERROR, MESSAGE_NOT_VALID_FIELDS) in flashes


def test_edit_note(authenticated_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any], note_repository: NoteRepository) -> None:
    new_content = "pepe"

    notes = note_repository.get_notes()
    last_note = notes[len(notes) - 1]
    last_note_content = last_note.content

    assert last_note

    response: Response = authenticated_client.put(
        f"{blueprints['notes']}/edit/{last_note.id}", 
        json={
            "content": new_content
        }
    )

    status_code = response.status_code
    data = response.get_json()

    assert status_code == 200
    assert data.get("message") == MESSAGE_EDIT_NOTE
    assert data.get("code") == CODE_EDIT_NOTE
    assert data.get("redirect_to") == flask_app.config["HOME_VIEW_PATH"]

    with authenticated_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert (FLASH_SUCCESS, MESSAGE_EDIT_NOTE) in flashes

    note = note_repository.get_note_by_id(id=last_note.id)
    note_content = note.content

    assert note_content == new_content
    assert note_content != last_note_content


def test_delete_note_invalid_id(authenticated_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any]) -> None:
    id = "asd"

    response: Response = authenticated_client.delete(
        f"{blueprints['notes']}/delete/{id}"
    )

    status_code = response.status_code
    data = response.get_json()

    assert status_code == 400
    assert data.get("message") == MESSAGE_NOT_VALID_ID
    assert data.get("code") == CODE_NOT_VALID_ID
    assert data.get("redirect_to") == flask_app.config["HOME_VIEW_PATH"]

    with authenticated_client.session_transaction() as session:
        flashes = session.get("_flashes")

        assert (FLASH_ERROR, MESSAGE_NOT_VALID_ID) in flashes


def test_delete_note_not_found_note(authenticated_client: FlaskClient, flask_app: Flask, blueprints: dict[str, Any]) -> None:
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


