from functools import wraps
from typing import Any, Callable, TypeVar, cast

from flask import Response, flash, redirect, request
from sqlalchemy.exc import SQLAlchemyError

from config.logger_config import setup_logger
from src.constants.codes import FLASH_ERROR
from src.constants.messages import (
    MESSAGE_ERROR_API,
    MESSAGE_ERROR_DATABASE,
    MESSAGE_ERROR_GENERIC,
)
from src.utils.exceptions import BaseAPIError

logger = setup_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def handle_exceptions(func: F) -> F:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Response:
        try:
            return func(*args, **kwargs)

        except BaseAPIError as e:
            logger.info(e)
            flash(MESSAGE_ERROR_API, FLASH_ERROR)
            return redirect(request.url)

        except SQLAlchemyError as e:
            logger.info(e)
            flash(MESSAGE_ERROR_DATABASE, FLASH_ERROR)
            return redirect(request.url)

        except Exception as e:
            flash(MESSAGE_ERROR_GENERIC.format(e=str(e)), FLASH_ERROR)
            return redirect(request.url)

    return cast(F, wrapper)
