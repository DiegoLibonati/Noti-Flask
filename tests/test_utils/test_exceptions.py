from typing import Any

import pytest
from flask import Flask

from src.utils.exceptions import (
    AuthenticationAPIError,
    BaseAPIError,
    BusinessAPIError,
    ConflictAPIError,
    InternalAPIError,
    NotFoundAPIError,
    ValidationAPIError,
)


class TestBaseAPIError:
    @pytest.mark.unit
    def test_default_status_code_is_500(self) -> None:
        error: BaseAPIError = BaseAPIError()
        assert error.status_code == 500

    @pytest.mark.unit
    def test_custom_status_code(self) -> None:
        error: BaseAPIError = BaseAPIError(status_code=418)
        assert error.status_code == 418

    @pytest.mark.unit
    def test_custom_message(self) -> None:
        error: BaseAPIError = BaseAPIError(message="custom msg")
        assert error.message == "custom msg"

    @pytest.mark.unit
    def test_custom_code(self) -> None:
        error: BaseAPIError = BaseAPIError(code="MY_CODE")
        assert error.code == "MY_CODE"

    @pytest.mark.unit
    def test_payload_defaults_to_empty_dict(self) -> None:
        error: BaseAPIError = BaseAPIError()
        assert error.payload == {}

    @pytest.mark.unit
    def test_custom_payload(self) -> None:
        error: BaseAPIError = BaseAPIError(payload={"field": "value"})
        assert error.payload == {"field": "value"}

    @pytest.mark.unit
    def test_to_dict_has_code_and_message(self) -> None:
        error: BaseAPIError = BaseAPIError(code="ERR", message="msg")
        result: dict[str, Any] = error.to_dict()
        assert result["code"] == "ERR"
        assert result["message"] == "msg"

    @pytest.mark.unit
    def test_to_dict_includes_payload_when_present(self) -> None:
        error: BaseAPIError = BaseAPIError(payload={"key": "val"})
        result: dict[str, Any] = error.to_dict()
        assert "payload" in result
        assert result["payload"]["key"] == "val"

    @pytest.mark.unit
    def test_to_dict_excludes_payload_when_empty(self) -> None:
        error: BaseAPIError = BaseAPIError()
        result: dict[str, Any] = error.to_dict()
        assert "payload" not in result

    @pytest.mark.unit
    def test_is_exception_subclass(self) -> None:
        error: BaseAPIError = BaseAPIError()
        assert isinstance(error, Exception)

    @pytest.mark.unit
    def test_flask_response_returns_tuple(self, app: Flask) -> None:
        with app.app_context():
            error: BaseAPIError = BaseAPIError(code="ERR", message="msg")
            response, status = error.flask_response()
            assert status == 500

    @pytest.mark.unit
    def test_flask_response_json_matches_to_dict(self, app: Flask) -> None:
        with app.app_context():
            error: BaseAPIError = BaseAPIError(code="ERR", message="msg")
            response, _ = error.flask_response()
            data: dict[str, Any] = response.get_json()
            assert data == error.to_dict()


class TestExceptionSubclasses:
    @pytest.mark.unit
    def test_validation_error_has_status_400(self) -> None:
        assert ValidationAPIError.status_code == 400

    @pytest.mark.unit
    def test_authentication_error_has_status_401(self) -> None:
        assert AuthenticationAPIError.status_code == 401

    @pytest.mark.unit
    def test_not_found_error_has_status_404(self) -> None:
        assert NotFoundAPIError.status_code == 404

    @pytest.mark.unit
    def test_conflict_error_has_status_409(self) -> None:
        assert ConflictAPIError.status_code == 409

    @pytest.mark.unit
    def test_business_error_has_status_422(self) -> None:
        assert BusinessAPIError.status_code == 422

    @pytest.mark.unit
    def test_internal_error_has_status_500(self) -> None:
        assert InternalAPIError.status_code == 500

    @pytest.mark.unit
    def test_all_subclasses_inherit_from_base(self) -> None:
        for cls in [ValidationAPIError, AuthenticationAPIError, NotFoundAPIError, ConflictAPIError, BusinessAPIError, InternalAPIError]:
            assert issubclass(cls, BaseAPIError)

    @pytest.mark.unit
    def test_subclass_accepts_custom_message(self) -> None:
        error: ValidationAPIError = ValidationAPIError(message="bad input")
        assert error.message == "bad input"

    @pytest.mark.unit
    def test_subclass_accepts_custom_code(self) -> None:
        error: NotFoundAPIError = NotFoundAPIError(code="NOT_FOUND_ITEM")
        assert error.code == "NOT_FOUND_ITEM"
