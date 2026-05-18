from collections.abc import Callable
from functools import wraps
from typing import Any

from sqlalchemy.exc import SQLAlchemyError

from src.configs.logger_config import setup_logger
from src.constants.codes import CODE_ERROR_DATABASE, CODE_ERROR_GENERIC
from src.constants.messages import MESSAGE_ERROR_DATABASE, MESSAGE_ERROR_GENERIC
from src.utils.exceptions import BaseAPIError, InternalAPIError

logger = setup_logger(__name__)


def exceptions_decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return fn(*args, **kwargs)

        except BaseAPIError:
            logger.debug("Domain API error propagated", exc_info=True)
            raise

        except SQLAlchemyError as e:
            logger.error("Database error", exc_info=e)
            raise InternalAPIError(code=CODE_ERROR_DATABASE, message=MESSAGE_ERROR_DATABASE) from e

        except Exception as e:
            logger.error("Unexpected error", exc_info=e)
            raise InternalAPIError(code=CODE_ERROR_GENERIC, message=MESSAGE_ERROR_GENERIC) from e

    return wrapper
