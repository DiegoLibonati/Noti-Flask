from typing import Any

import pytest

from src.constants.codes import CODE_ERROR_API
from src.constants.messages import MESSAGE_ERROR_API
from src.utils.exceptions import (
    AuthenticationAPIError,
    BaseAPIError,
    ConflictAPIError,
    NotFoundAPIError,
    ValidationAPIError,
)


def test_base_api_error_defaults() -> None:
    err = BaseAPIError()
    body: dict[str, Any] = err.to_dict()

    assert err.status_code == 500
    assert err.code == CODE_ERROR_API
    assert err.message == MESSAGE_ERROR_API
    assert isinstance(body, dict)
    assert body["code"] == CODE_ERROR_API
    assert body["message"] == MESSAGE_ERROR_API
    assert body["payload"] == {}


def test_base_api_error_overrides() -> None:
    err = BaseAPIError(
        code="CUSTOM_CODE",
        message="Custom message",
        status_code=418,
        payload={"x": 1},
    )
    body: dict[str, Any] = err.to_dict()

    assert err.status_code == 418
    assert err.code == "CUSTOM_CODE"
    assert err.message == "Custom message"
    assert body["payload"] == {"x": 1}


@pytest.mark.parametrize(
    "exc_cls,expected_status,expected_message",
    [
        (ValidationAPIError, 400, "Validation error"),
        (AuthenticationAPIError, 401, "Authentication error"),
        (NotFoundAPIError, 404, "Resource not found"),
        (ConflictAPIError, 409, "Conflict error"),
    ],
)
def test_specific_errors(
    exc_cls: type[BaseAPIError], expected_status: int, expected_message: str
) -> None:
    err = exc_cls()
    body: dict[str, Any] = err.to_dict()

    assert err.status_code == expected_status
    assert err.message == expected_message
    assert body["code"] == err.code
    assert body["message"] == expected_message
