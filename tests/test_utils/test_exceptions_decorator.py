import logging

import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.constants.codes import CODE_ERROR_DATABASE, CODE_ERROR_GENERIC
from src.utils.exceptions import BaseAPIError, InternalAPIError, ValidationAPIError
from src.utils.exceptions_decorator import exceptions_decorator


class TestExceptionsDecorator:
    @pytest.mark.unit
    def test_passes_through_base_api_error_unchanged(self) -> None:
        @exceptions_decorator
        def fn() -> None:
            raise ValidationAPIError(code="VAL", message="bad")

        with pytest.raises(ValidationAPIError) as exc_info:
            fn()
        assert exc_info.value.code == "VAL"

    @pytest.mark.unit
    def test_passes_through_any_base_api_error_subclass(self) -> None:
        @exceptions_decorator
        def fn() -> None:
            raise BaseAPIError(status_code=418)

        with pytest.raises(BaseAPIError) as exc_info:
            fn()
        assert exc_info.value.status_code == 418

    @pytest.mark.unit
    def test_converts_sqlalchemy_error_to_internal_api_error(self, caplog) -> None:
        @exceptions_decorator
        def fn() -> None:
            raise SQLAlchemyError("connection failed")

        with caplog.at_level(logging.CRITICAL, logger="src.utils.exceptions_decorator"):
            with pytest.raises(InternalAPIError):
                fn()

    @pytest.mark.unit
    def test_sqlalchemy_error_uses_database_code(self, caplog) -> None:
        @exceptions_decorator
        def fn() -> None:
            raise SQLAlchemyError("boom")

        with caplog.at_level(logging.CRITICAL, logger="src.utils.exceptions_decorator"):
            with pytest.raises(InternalAPIError) as exc_info:
                fn()
        assert exc_info.value.code == CODE_ERROR_DATABASE

    @pytest.mark.unit
    def test_converts_generic_exception_to_internal_api_error(self, caplog) -> None:
        @exceptions_decorator
        def fn() -> None:
            raise RuntimeError("unexpected")

        with caplog.at_level(logging.CRITICAL, logger="src.utils.exceptions_decorator"):
            with pytest.raises(InternalAPIError):
                fn()

    @pytest.mark.unit
    def test_generic_exception_uses_generic_code(self, caplog) -> None:
        @exceptions_decorator
        def fn() -> None:
            raise RuntimeError("boom")

        with caplog.at_level(logging.CRITICAL, logger="src.utils.exceptions_decorator"):
            with pytest.raises(InternalAPIError) as exc_info:
                fn()
        assert exc_info.value.code == CODE_ERROR_GENERIC

    @pytest.mark.unit
    def test_preserves_return_value_on_success(self) -> None:
        @exceptions_decorator
        def fn() -> str:
            return "ok"

        result: str = fn()
        assert result == "ok"

    @pytest.mark.unit
    def test_passes_args_and_kwargs_to_wrapped_function(self) -> None:
        @exceptions_decorator
        def fn(a: int, b: int = 0) -> int:
            return a + b

        result: int = fn(2, b=3)
        assert result == 5

    @pytest.mark.unit
    def test_preserves_function_name(self) -> None:
        @exceptions_decorator
        def my_function() -> None:
            pass

        assert my_function.__name__ == "my_function"

    @pytest.mark.unit
    def test_sqlalchemy_error_chained_as_cause(self) -> None:
        original: SQLAlchemyError = SQLAlchemyError("db down")

        @exceptions_decorator
        def fn() -> None:
            raise original

        with pytest.raises(InternalAPIError) as exc_info:
            fn()
        assert exc_info.value.__cause__ is original

    @pytest.mark.unit
    def test_generic_error_chained_as_cause(self) -> None:
        original: RuntimeError = RuntimeError("kaboom")

        @exceptions_decorator
        def fn() -> None:
            raise original

        with pytest.raises(InternalAPIError) as exc_info:
            fn()
        assert exc_info.value.__cause__ is original
