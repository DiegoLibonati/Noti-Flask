import logging
from unittest.mock import MagicMock, patch

import pytest

from src.utils.commit_or_rollback_decorator import commit_or_rollback_decorator


class TestCommitOrRollbackDecorator:
    @pytest.mark.unit
    def test_commits_when_function_succeeds(self) -> None:
        with patch("src.utils.commit_or_rollback_decorator.db") as mock_db:

            @commit_or_rollback_decorator("adding thing")
            def fn() -> str:
                return "done"

            result: str = fn()

        assert result == "done"
        mock_db.session.commit.assert_called_once()
        mock_db.session.rollback.assert_not_called()

    @pytest.mark.unit
    def test_rolls_back_when_function_raises(self, caplog) -> None:
        with patch("src.utils.commit_or_rollback_decorator.db") as mock_db:

            @commit_or_rollback_decorator("breaking thing")
            def fn() -> None:
                raise ValueError("boom")

            with caplog.at_level(logging.CRITICAL, logger="src.utils.commit_or_rollback_decorator"):
                with pytest.raises(ValueError, match="boom"):
                    fn()

        mock_db.session.commit.assert_not_called()
        mock_db.session.rollback.assert_called_once()

    @pytest.mark.unit
    def test_rolls_back_and_reraises_original_exception(self, caplog) -> None:
        original: RuntimeError = RuntimeError("explode")

        with patch("src.utils.commit_or_rollback_decorator.db"):

            @commit_or_rollback_decorator("kaboom action")
            def fn() -> None:
                raise original

            with caplog.at_level(logging.CRITICAL, logger="src.utils.commit_or_rollback_decorator"):
                with pytest.raises(RuntimeError) as exc_info:
                    fn()

        assert exc_info.value is original

    @pytest.mark.unit
    def test_logs_error_with_action_label_on_failure(self, caplog) -> None:
        with patch("src.utils.commit_or_rollback_decorator.db"):

            @commit_or_rollback_decorator("updating user")
            def fn() -> None:
                raise ValueError("bad data")

            with caplog.at_level(logging.ERROR, logger="src.utils.commit_or_rollback_decorator"):
                with pytest.raises(ValueError):
                    fn()

        assert any("updating user" in record.message for record in caplog.records)

    @pytest.mark.unit
    def test_passes_args_and_kwargs_to_wrapped_function(self) -> None:
        captured: dict = {}

        with patch("src.utils.commit_or_rollback_decorator.db"):

            @commit_or_rollback_decorator("computing")
            def fn(a: int, b: int = 0) -> int:
                captured["a"] = a
                captured["b"] = b
                return a + b

            result: int = fn(3, b=4)

        assert result == 7
        assert captured == {"a": 3, "b": 4}

    @pytest.mark.unit
    def test_preserves_function_name(self) -> None:
        @commit_or_rollback_decorator("doing")
        def my_function() -> None:
            pass

        assert my_function.__name__ == "my_function"

    @pytest.mark.unit
    def test_returns_unmodified_value_from_wrapped_function(self) -> None:
        sentinel: object = object()

        with patch("src.utils.commit_or_rollback_decorator.db"):

            @commit_or_rollback_decorator("identity")
            def fn() -> object:
                return sentinel

            result: object = fn()

        assert result is sentinel

    @pytest.mark.unit
    def test_decorator_factory_returns_callable(self) -> None:
        decorator = commit_or_rollback_decorator("anything")

        def fn() -> None:
            return None

        wrapped = decorator(fn)
        assert callable(wrapped)

    @pytest.mark.unit
    def test_does_not_swallow_base_exception_subclasses(self, caplog) -> None:
        with patch("src.utils.commit_or_rollback_decorator.db") as mock_db:

            @commit_or_rollback_decorator("custom")
            def fn() -> None:
                raise KeyError("missing")

            with caplog.at_level(logging.CRITICAL, logger="src.utils.commit_or_rollback_decorator"):
                with pytest.raises(KeyError):
                    fn()

        mock_db.session.rollback.assert_called_once()

    @pytest.mark.unit
    def test_each_invocation_calls_commit_independently(self) -> None:
        with patch("src.utils.commit_or_rollback_decorator.db") as mock_db:

            @commit_or_rollback_decorator("invocations")
            def fn() -> int:
                return 1

            fn()
            fn()
            fn()

        assert mock_db.session.commit.call_count == 3

    @pytest.mark.unit
    def test_does_not_call_rollback_when_commit_succeeds(self) -> None:
        mock_db: MagicMock = MagicMock()
        with patch("src.utils.commit_or_rollback_decorator.db", mock_db):

            @commit_or_rollback_decorator("ok action")
            def fn() -> None:
                return None

            fn()

        mock_db.session.rollback.assert_not_called()
