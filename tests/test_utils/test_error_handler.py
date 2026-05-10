import logging

import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.utils.error_handler import handle_exceptions
from src.utils.exceptions import BaseAPIError, InternalAPIError, ValidationAPIError


class TestHandleExceptions:
    @pytest.mark.unit
    def test_passes_through_base_api_error_unchanged(self) -> None:
        @handle_exceptions
        def fn():
            raise ValidationAPIError(code="VAL", message="bad")

        with pytest.raises(ValidationAPIError) as exc_info:
            fn()
        assert exc_info.value.code == "VAL"

    @pytest.mark.unit
    def test_passes_through_any_base_api_error_subclass(self) -> None:
        @handle_exceptions
        def fn():
            raise BaseAPIError(status_code=418)

        with pytest.raises(BaseAPIError) as exc_info:
            fn()
        assert exc_info.value.status_code == 418

    @pytest.mark.unit
    def test_converts_sqlalchemy_error_to_internal_api_error(self, caplog) -> None:
        @handle_exceptions
        def fn():
            raise SQLAlchemyError("connection failed")

        with caplog.at_level(logging.CRITICAL, logger="src.utils.error_handler"):
            with pytest.raises(InternalAPIError):
                fn()

    @pytest.mark.unit
    def test_converts_generic_exception_to_internal_api_error(self, caplog) -> None:
        @handle_exceptions
        def fn():
            raise RuntimeError("unexpected")

        with caplog.at_level(logging.CRITICAL, logger="src.utils.error_handler"):
            with pytest.raises(InternalAPIError):
                fn()

    @pytest.mark.unit
    def test_preserves_return_value_on_success(self) -> None:
        @handle_exceptions
        def fn() -> str:
            return "ok"

        result: str = fn()
        assert result == "ok"

    @pytest.mark.unit
    def test_passes_args_and_kwargs_to_wrapped_function(self) -> None:
        @handle_exceptions
        def fn(a: int, b: int = 0) -> int:
            return a + b

        result: int = fn(2, b=3)
        assert result == 5

    @pytest.mark.unit
    def test_preserves_function_name(self) -> None:
        @handle_exceptions
        def my_function() -> None:
            pass

        assert my_function.__name__ == "my_function"
