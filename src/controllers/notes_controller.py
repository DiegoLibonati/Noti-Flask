import logging
import re

from flask import Response
from flask import flash
from flask import current_app
from flask import make_response
from flask import request
from flask_login import current_user

from src.data_access.note_repository import NoteRepository
from src.utils.constants import FLASH_SUCCESS
from src.utils.constants import FLASH_ERROR
from src.utils.constants import CODE_CREATE_NOTE
from src.utils.constants import CODE_DELETE_NOTE
from src.utils.constants import CODE_EDIT_NOTE
from src.utils.constants import CODE_NOT_EXISTS_NOTE
from src.utils.constants import CODE_NOT_VALID_ID
from src.utils.constants import CODE_NOT_VALID_FIELDS
from src.utils.constants import CODE_ERROR_DELETE_NOTE
from src.utils.constants import CODE_ERROR_UPDATE_NOTE
from src.utils.constants import MESSAGE_CREATE_NOTE
from src.utils.constants import MESSAGE_DELETE_NOTE
from src.utils.constants import MESSAGE_EDIT_NOTE
from src.utils.constants import MESSAGE_NOT_EXISTS_NOTE
from src.utils.constants import MESSAGE_NOT_VALID_ID
from src.utils.constants import MESSAGE_NOT_VALID_FIELDS
from src.utils.constants import MESSAGE_ERROR_DELETE_NOTE
from src.utils.constants import MESSAGE_ERROR_UPDATE_NOTE


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def create() -> Response:
    user_id = current_user.id
    note_repository = NoteRepository()

    note_repository.add_note(user_id=user_id)

    flash(MESSAGE_CREATE_NOTE, FLASH_SUCCESS)

    response = {
        "message": MESSAGE_CREATE_NOTE,
        "code": CODE_CREATE_NOTE,
        "redirect_to": current_app.config["HOME_VIEW_PATH"]
    }
    status_code = 201
    
    return make_response(response, status_code)


def delete(id: str) -> Response:
    if not id or not re.fullmatch(r"\d+", id):
        flash(MESSAGE_NOT_VALID_ID, FLASH_ERROR)
        
        response = {
            "message": MESSAGE_NOT_VALID_ID,
            "code": CODE_NOT_VALID_ID,
            "redirect_to": current_app.config["HOME_VIEW_PATH"]
        }
        status_code = 400

        return make_response(response, status_code)

    note_id = int(id)
    note_repository = NoteRepository()

    note = note_repository.get_note_by_id(id=note_id)

    if not note:
        flash(MESSAGE_NOT_EXISTS_NOTE, FLASH_ERROR)

        response = {
            "message": MESSAGE_NOT_EXISTS_NOTE,
            "code": CODE_NOT_EXISTS_NOTE,
            "redirect_to": current_app.config["HOME_VIEW_PATH"]
        }
        status_code = 404

        return make_response(response, status_code)


    status = note_repository.remove_note(note=note)

    if not status:
        flash(MESSAGE_ERROR_DELETE_NOTE, FLASH_ERROR)

        response = {
            "message": MESSAGE_ERROR_DELETE_NOTE,
            "code": CODE_ERROR_DELETE_NOTE,
            "redirect_to": current_app.config["HOME_VIEW_PATH"]
        }
        status_code = 400

        return make_response(response, status_code)

    flash(MESSAGE_DELETE_NOTE, FLASH_SUCCESS)

    response = {
        "message": MESSAGE_DELETE_NOTE,
        "code": CODE_DELETE_NOTE,
        "redirect_to": current_app.config["HOME_VIEW_PATH"]
    }
    status_code = 200
    
    return make_response(response, status_code)


def edit(id: str) -> Response:
    if not id or not re.fullmatch(r"\d+", id):
        flash(MESSAGE_NOT_VALID_ID, FLASH_ERROR)
        
        response = {
            "message": MESSAGE_NOT_VALID_ID,
            "code": CODE_NOT_VALID_ID,
            "redirect_to": current_app.config["HOME_VIEW_PATH"]
        }
        status_code = 400

        return make_response(response, status_code)
    
    body = request.get_json()

    note_id = int(id)
    note_content = body.get("content", None)

    if not note_content:
        flash(MESSAGE_NOT_VALID_FIELDS, FLASH_ERROR)

        response = {
            "message": MESSAGE_NOT_VALID_FIELDS,
            "code": CODE_NOT_VALID_FIELDS,
            "redirect_to": current_app.config["HOME_VIEW_PATH"]
        }
        status_code = 400

        return make_response(response, status_code)

    note_repository = NoteRepository()

    note = note_repository.get_note_by_id(id=note_id)

    if not note:
        flash(MESSAGE_NOT_EXISTS_NOTE, FLASH_ERROR)

        response = {
            "message": MESSAGE_NOT_EXISTS_NOTE,
            "code": CODE_NOT_EXISTS_NOTE,
            "redirect_to": current_app.config["HOME_VIEW_PATH"]
        }
        status_code = 404

        return make_response(response, status_code)

    status = note_repository.update_note_content_by_id(id_note=note_id, content=note_content.strip())

    if not status:
        flash(MESSAGE_ERROR_UPDATE_NOTE, FLASH_ERROR)

        response = {
            "message": MESSAGE_ERROR_UPDATE_NOTE,
            "code": CODE_ERROR_UPDATE_NOTE,
            "redirect_to": current_app.config["HOME_VIEW_PATH"]
        }
        status_code = 400

        return make_response(response, status_code)

    flash(MESSAGE_EDIT_NOTE, FLASH_SUCCESS)

    response = {
        "message": MESSAGE_EDIT_NOTE,
        "code": CODE_EDIT_NOTE,
        "redirect_to": current_app.config["HOME_VIEW_PATH"]
    }
    status_code = 200
    
    return make_response(response, status_code)
