from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

from src.configs.logger_config import setup_logger
from src.configs.sql_alchemy_config import db

logger = setup_logger(__name__)

P = ParamSpec("P")
T = TypeVar("T")


def commit_or_rollback_decorator(action_label: str) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorator(fn: Callable[P, T]) -> Callable[P, T]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                result = fn(*args, **kwargs)
                db.session.commit()
                return result
            except Exception as ex:
                db.session.rollback()
                logger.error("Error %s", action_label, exc_info=ex)
                raise

        return wrapper

    return decorator
