import pytest

from src.constants import messages


class TestSuccessMessages:
    @pytest.mark.unit
    @pytest.mark.parametrize(
        "name",
        [
            "MESSAGE_SUCCESS_HEALTH",
            "MESSAGE_SUCCESS_READY",
            "MESSAGE_SUCCESS_GET_ALL_NOTES",
            "MESSAGE_SUCCESS_ADD_NOTE",
            "MESSAGE_SUCCESS_DELETE_NOTE",
            "MESSAGE_SUCCESS_EDIT_NOTE",
            "MESSAGE_SUCCESS_LOGGED_IN",
            "MESSAGE_SUCCESS_LOGOUT",
            "MESSAGE_SUCCESS_SIGN_UP",
        ],
    )
    def test_success_message_is_non_empty_string(self, name: str) -> None:
        value = getattr(messages, name)
        assert isinstance(value, str)
        assert len(value) > 0


class TestErrorMessages:
    @pytest.mark.unit
    @pytest.mark.parametrize(
        "name",
        [
            "MESSAGE_ERROR_INTERNAL_SERVER",
            "MESSAGE_ERROR_DATABASE",
            "MESSAGE_ERROR_GENERIC",
        ],
    )
    def test_error_message_is_non_empty_string(self, name: str) -> None:
        value = getattr(messages, name)
        assert isinstance(value, str)
        assert len(value) > 0


class TestNotValidMessages:
    @pytest.mark.unit
    @pytest.mark.parametrize(
        "name",
        [
            "MESSAGE_NOT_VALID_INTEGER",
            "MESSAGE_NOT_VALID_FIELDS",
            "MESSAGE_NOT_VALID_PASSWORD",
        ],
    )
    def test_not_valid_message_is_non_empty_string(self, name: str) -> None:
        value = getattr(messages, name)
        assert isinstance(value, str)
        assert len(value) > 0


class TestAlreadyExistsMessages:
    @pytest.mark.unit
    @pytest.mark.parametrize(
        "name",
        [
            "MESSAGE_ALREADY_EXISTS_NOTE",
            "MESSAGE_ALREADY_EXISTS_USER",
        ],
    )
    def test_already_exists_message_is_non_empty_string(self, name: str) -> None:
        value = getattr(messages, name)
        assert isinstance(value, str)
        assert len(value) > 0


class TestNotFoundMessages:
    @pytest.mark.unit
    @pytest.mark.parametrize(
        "name",
        [
            "MESSAGE_NOT_FOUND_ROUTE",
            "MESSAGE_NOT_FOUND_NOTE",
            "MESSAGE_NOT_FOUND_USER",
        ],
    )
    def test_not_found_message_is_non_empty_string(self, name: str) -> None:
        value = getattr(messages, name)
        assert isinstance(value, str)
        assert len(value) > 0


class TestMessagesContent:
    @pytest.mark.unit
    def test_health_message_mentions_healthy(self) -> None:
        assert "healthy" in messages.MESSAGE_SUCCESS_HEALTH.lower()

    @pytest.mark.unit
    def test_ready_message_mentions_ready(self) -> None:
        assert "ready" in messages.MESSAGE_SUCCESS_READY.lower()

    @pytest.mark.unit
    def test_logged_in_message_mentions_logged_in(self) -> None:
        assert "logged in" in messages.MESSAGE_SUCCESS_LOGGED_IN.lower()

    @pytest.mark.unit
    def test_not_found_user_message_mentions_user(self) -> None:
        assert "user" in messages.MESSAGE_NOT_FOUND_USER.lower()

    @pytest.mark.unit
    def test_not_found_note_message_mentions_note(self) -> None:
        assert "note" in messages.MESSAGE_NOT_FOUND_NOTE.lower()
