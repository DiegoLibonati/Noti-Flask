from flask import current_app, flash, jsonify, request
from flask.typing import ResponseReturnValue
from flask_login import current_user, login_required

from src.constants.codes import (
    CODE_NOT_FOUND_NOTE,
    CODE_NOT_VALID_FIELDS,
    CODE_NOT_VALID_INTEGER,
    CODE_SUCCESS_ADD_NOTE,
    CODE_SUCCESS_DELETE_NOTE,
    CODE_SUCCESS_EDIT_NOTE,
    CODE_SUCCESS_GET_ALL_NOTES,
    FLASH_ERROR,
    FLASH_SUCCESS,
)
from src.constants.messages import (
    MESSAGE_NOT_FOUND_NOTE,
    MESSAGE_NOT_VALID_FIELDS,
    MESSAGE_NOT_VALID_INTEGER,
    MESSAGE_SUCCESS_ADD_NOTE,
    MESSAGE_SUCCESS_DELETE_NOTE,
    MESSAGE_SUCCESS_EDIT_NOTE,
    MESSAGE_SUCCESS_GET_ALL_NOTES,
)
from src.models.orm.note import Note
from src.services.note_service import NoteService
from src.utils.exceptions import NotFoundAPIError, ValidationAPIError
from src.utils.exceptions_decorator import exceptions_decorator


@exceptions_decorator
def alive() -> ResponseReturnValue:
    response = {
        "message": "I am Alive!",
        "version_bp": "1.0.0",
        "name_bp": "Notes",
    }
    return jsonify(response), 200


@exceptions_decorator
def get_all() -> ResponseReturnValue:
    notes = NoteService.get_all_notes()
    response = {
        "code": CODE_SUCCESS_GET_ALL_NOTES,
        "message": MESSAGE_SUCCESS_GET_ALL_NOTES,
        "data": [note.to_dict() for note in notes],
    }
    return jsonify(response), 200


@login_required
@exceptions_decorator
def create() -> ResponseReturnValue:
    body = request.get_json(silent=True) or {}
    content = body.get("content", "").strip()

    note = Note(content=content, user_id=current_user.id)
    NoteService.add_note(note)

    flash(MESSAGE_SUCCESS_ADD_NOTE, FLASH_SUCCESS)
    response = {
        "code": CODE_SUCCESS_ADD_NOTE,
        "message": MESSAGE_SUCCESS_ADD_NOTE,
        "redirect_to": current_app.config["HOME_VIEW_PATH"],
    }
    return jsonify(response), 201


@login_required
@exceptions_decorator
def delete(id: str) -> ResponseReturnValue:
    try:
        note_id = int(id)
    except (ValueError, TypeError):
        flash(MESSAGE_NOT_VALID_INTEGER, FLASH_ERROR)
        raise ValidationAPIError(code=CODE_NOT_VALID_INTEGER, message=MESSAGE_NOT_VALID_INTEGER) from None

    note = NoteService.get_note_by_id(id=note_id)

    if not note:
        flash(MESSAGE_NOT_FOUND_NOTE, FLASH_ERROR)
        raise NotFoundAPIError(code=CODE_NOT_FOUND_NOTE, message=MESSAGE_NOT_FOUND_NOTE)

    NoteService.delete_note(note=note)

    flash(MESSAGE_SUCCESS_DELETE_NOTE, FLASH_SUCCESS)
    response = {
        "code": CODE_SUCCESS_DELETE_NOTE,
        "message": MESSAGE_SUCCESS_DELETE_NOTE,
        "redirect_to": current_app.config["HOME_VIEW_PATH"],
    }
    return jsonify(response), 200


@login_required
@exceptions_decorator
def edit(id: str) -> ResponseReturnValue:
    try:
        note_id = int(id)
    except (ValueError, TypeError):
        flash(MESSAGE_NOT_VALID_INTEGER, FLASH_ERROR)
        raise ValidationAPIError(code=CODE_NOT_VALID_INTEGER, message=MESSAGE_NOT_VALID_INTEGER) from None

    body = request.get_json()
    content = body.get("content", "").strip() if body else ""

    if not content:
        flash(MESSAGE_NOT_VALID_FIELDS, FLASH_ERROR)
        raise ValidationAPIError(code=CODE_NOT_VALID_FIELDS, message=MESSAGE_NOT_VALID_FIELDS)

    note = NoteService.get_note_by_id(id=note_id)

    if not note:
        flash(MESSAGE_NOT_FOUND_NOTE, FLASH_ERROR)
        raise NotFoundAPIError(code=CODE_NOT_FOUND_NOTE, message=MESSAGE_NOT_FOUND_NOTE)

    NoteService.update_note(note, {"content": content})

    flash(MESSAGE_SUCCESS_EDIT_NOTE, FLASH_SUCCESS)
    response = {
        "code": CODE_SUCCESS_EDIT_NOTE,
        "message": MESSAGE_SUCCESS_EDIT_NOTE,
        "redirect_to": current_app.config["HOME_VIEW_PATH"],
    }
    return jsonify(response), 200
