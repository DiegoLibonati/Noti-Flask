import re

from flask import Response, current_app, flash, jsonify, redirect, request, url_for
from flask_login import current_user, login_required

from src.constants.codes import (
    CODE_DELETE_NOTE,
    CODE_EDIT_NOTE,
    CODE_ERROR_DELETE_NOTE,
    CODE_ERROR_UPDATE_NOTE,
    CODE_NOT_EXISTS_NOTE,
    CODE_NOT_VALID_FIELDS,
    CODE_NOT_VALID_ID,
    FLASH_ERROR,
    FLASH_SUCCESS,
)
from src.constants.messages import (
    MESSAGE_CREATE_NOTE,
    MESSAGE_DELETE_NOTE,
    MESSAGE_EDIT_NOTE,
    MESSAGE_ERROR_DELETE_NOTE,
    MESSAGE_ERROR_UPDATE_NOTE,
    MESSAGE_NOT_EXISTS_NOTE,
    MESSAGE_NOT_VALID_FIELDS,
    MESSAGE_NOT_VALID_ID,
)
from src.models.orm.note import Note
from src.services.note_service import NoteService
from src.utils.error_handler import handle_exceptions


@handle_exceptions
def alive() -> Response:
    response = {
        "message": "I am Alive!",
        "version_bp": "2.0.0",
        "author": "Diego Libonati",
        "name_bp": "Note",
    }

    return jsonify(response), 200


@login_required
@handle_exceptions
def create() -> Response:
    user_id = current_user.id

    note = Note(content="", user_id=user_id)

    NoteService.add_note(note)

    flash(MESSAGE_CREATE_NOTE, FLASH_SUCCESS)
    return redirect(url_for(current_app.config["HOME_VIEW"]))


@login_required
@handle_exceptions
def delete(id: str) -> Response:
    if not id or not re.fullmatch(r"\d+", id):
        flash(MESSAGE_NOT_VALID_ID, FLASH_ERROR)
        response = {
            "code": CODE_NOT_VALID_ID,
            "message": MESSAGE_NOT_VALID_ID,
            "redirect_to": current_app.config["HOME_VIEW_PATH"],
        }

        return jsonify(response), 400

    note_id = int(id)

    note = NoteService.get_note_by_id(id=note_id)

    if not note:
        flash(MESSAGE_NOT_EXISTS_NOTE, FLASH_ERROR)
        response = {
            "code": CODE_NOT_EXISTS_NOTE,
            "message": MESSAGE_NOT_EXISTS_NOTE,
            "redirect_to": current_app.config["HOME_VIEW_PATH"],
        }

        return jsonify(response), 404

    status = NoteService.delete_note(note=note)

    if not status:
        flash(MESSAGE_ERROR_DELETE_NOTE, FLASH_ERROR)
        response = {
            "code": CODE_ERROR_DELETE_NOTE,
            "message": MESSAGE_ERROR_DELETE_NOTE,
            "redirect_to": current_app.config["HOME_VIEW_PATH"],
        }

        return jsonify(response), 400

    flash(MESSAGE_DELETE_NOTE, FLASH_SUCCESS)
    response = {
        "code": CODE_DELETE_NOTE,
        "message": MESSAGE_DELETE_NOTE,
        "redirect_to": current_app.config["HOME_VIEW_PATH"],
    }

    return jsonify(response), 200


@login_required
@handle_exceptions
def edit(id: str) -> Response:
    if not id or not re.fullmatch(r"\d+", id):
        flash(MESSAGE_NOT_VALID_ID, FLASH_ERROR)
        response = {
            "code": CODE_NOT_VALID_ID,
            "message": MESSAGE_NOT_VALID_ID,
            "redirect_to": current_app.config["HOME_VIEW_PATH"],
        }

        return jsonify(response), 400

    body = request.get_json()

    note_id = int(id)
    note_content = body.get("content", None)

    if not note_content:
        flash(MESSAGE_NOT_VALID_FIELDS, FLASH_ERROR)
        response = {
            "code": CODE_NOT_VALID_FIELDS,
            "message": MESSAGE_NOT_VALID_FIELDS,
            "redirect_to": current_app.config["HOME_VIEW_PATH"],
        }

        return jsonify(response), 400

    note = NoteService.get_note_by_id(id=note_id)

    if not note:
        flash(MESSAGE_NOT_EXISTS_NOTE, FLASH_ERROR)
        response = {
            "code": CODE_ERROR_DELETE_NOTE,
            "message": MESSAGE_ERROR_DELETE_NOTE,
            "redirect_to": current_app.config["HOME_VIEW_PATH"],
        }

        return jsonify(response), 400

    status = NoteService.update_note(note, {"content": note_content.strip()})

    if not status:
        flash(MESSAGE_ERROR_UPDATE_NOTE, FLASH_ERROR)
        response = {
            "code": CODE_ERROR_UPDATE_NOTE,
            "message": MESSAGE_ERROR_UPDATE_NOTE,
            "redirect_to": current_app.config["HOME_VIEW_PATH"],
        }

        return jsonify(response), 400

    flash(MESSAGE_EDIT_NOTE, FLASH_SUCCESS)
    response = {
        "code": CODE_EDIT_NOTE,
        "message": MESSAGE_EDIT_NOTE,
        "redirect_to": current_app.config["HOME_VIEW_PATH"],
    }

    return jsonify(response), 200
