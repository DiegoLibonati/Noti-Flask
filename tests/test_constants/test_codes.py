import pytest

from src.constants import codes


class TestFlashCodes:
    @pytest.mark.unit
    def test_flash_success_value(self) -> None:
        assert codes.FLASH_SUCCESS == "success"

    @pytest.mark.unit
    def test_flash_error_value(self) -> None:
        assert codes.FLASH_ERROR == "error"


class TestSuccessCodes:
    @pytest.mark.unit
    @pytest.mark.parametrize(
        "name,expected",
        [
            ("CODE_SUCCESS_HEALTH", "SUCCESS_HEALTH"),
            ("CODE_SUCCESS_READY", "SUCCESS_READY"),
            ("CODE_SUCCESS_GET_ALL_NOTES", "SUCCESS_GET_ALL_NOTES"),
            ("CODE_SUCCESS_ADD_NOTE", "SUCCESS_ADD_NOTE"),
            ("CODE_SUCCESS_DELETE_NOTE", "SUCCESS_DELETE_NOTE"),
            ("CODE_SUCCESS_EDIT_NOTE", "SUCCESS_EDIT_NOTE"),
            ("CODE_SUCCESS_LOGGED_IN", "SUCCESS_LOGGED_IN"),
            ("CODE_SUCCESS_LOGOUT", "SUCCESS_LOGOUT"),
            ("CODE_SUCCESS_SIGN_UP", "SUCCESS_SIGN_UP"),
        ],
    )
    def test_success_code_value(self, name: str, expected: str) -> None:
        assert getattr(codes, name) == expected


class TestErrorCodes:
    @pytest.mark.unit
    @pytest.mark.parametrize(
        "name,expected",
        [
            ("CODE_ERROR_INTERNAL_SERVER", "ERROR_INTERNAL_SERVER"),
            ("CODE_ERROR_DATABASE", "ERROR_DATABASE"),
            ("CODE_ERROR_GENERIC", "ERROR_GENERIC"),
        ],
    )
    def test_error_code_value(self, name: str, expected: str) -> None:
        assert getattr(codes, name) == expected


class TestNotValidCodes:
    @pytest.mark.unit
    @pytest.mark.parametrize(
        "name,expected",
        [
            ("CODE_NOT_VALID_INTEGER", "NOT_VALID_INTEGER"),
            ("CODE_NOT_VALID_FIELDS", "NOT_VALID_FIELDS"),
            ("CODE_NOT_VALID_PASSWORD", "NOT_VALID_PASSWORD"),
        ],
    )
    def test_not_valid_code_value(self, name: str, expected: str) -> None:
        assert getattr(codes, name) == expected


class TestAlreadyExistsCodes:
    @pytest.mark.unit
    @pytest.mark.parametrize(
        "name,expected",
        [
            ("CODE_ALREADY_EXISTS_NOTE", "ALREADY_EXISTS_NOTE"),
            ("CODE_ALREADY_EXISTS_USER", "ALREADY_EXISTS_USER"),
        ],
    )
    def test_already_exists_code_value(self, name: str, expected: str) -> None:
        assert getattr(codes, name) == expected


class TestNotFoundCodes:
    @pytest.mark.unit
    @pytest.mark.parametrize(
        "name,expected",
        [
            ("CODE_NOT_FOUND_ROUTE", "NOT_FOUND_ROUTE"),
            ("CODE_NOT_FOUND_NOTE", "NOT_FOUND_NOTE"),
            ("CODE_NOT_FOUND_USER", "NOT_FOUND_USER"),
        ],
    )
    def test_not_found_code_value(self, name: str, expected: str) -> None:
        assert getattr(codes, name) == expected


class TestCodesAreStrings:
    @pytest.mark.unit
    def test_all_codes_are_strings(self) -> None:
        for name in dir(codes):
            if name.startswith(("CODE_", "FLASH_")):
                assert isinstance(getattr(codes, name), str)

    @pytest.mark.unit
    def test_all_codes_are_non_empty(self) -> None:
        for name in dir(codes):
            if name.startswith(("CODE_", "FLASH_")):
                assert len(getattr(codes, name)) > 0
