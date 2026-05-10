import pytest

from src.services.encrypt_service import EncryptService


class TestEncryptService:
    @pytest.mark.unit
    def test_password_property_returns_plain_password(self) -> None:
        service: EncryptService = EncryptService("secret123")
        assert service.password == "secret123"

    @pytest.mark.unit
    def test_password_hashed_differs_from_plain(self) -> None:
        service: EncryptService = EncryptService("secret123")
        assert service.password_hashed != "secret123"

    @pytest.mark.unit
    def test_password_hashed_is_string(self) -> None:
        service: EncryptService = EncryptService("secret123")
        assert isinstance(service.password_hashed, str)

    @pytest.mark.unit
    def test_each_hash_is_unique(self) -> None:
        service: EncryptService = EncryptService("secret123")
        hash1: str = service.password_hashed
        hash2: str = service.password_hashed
        assert hash1 != hash2

    @pytest.mark.unit
    def test_valid_password_returns_true_for_correct_password(self) -> None:
        service: EncryptService = EncryptService("mypassword")
        hashed: str = service.password_hashed
        assert service.valid_password(hashed) is True

    @pytest.mark.unit
    def test_valid_password_returns_false_for_wrong_password(self) -> None:
        service: EncryptService = EncryptService("mypassword")
        hashed: str = service.password_hashed
        wrong_service: EncryptService = EncryptService("wrongpassword")
        assert wrong_service.valid_password(hashed) is False

    @pytest.mark.unit
    def test_valid_password_returns_false_for_empty_password(self) -> None:
        service: EncryptService = EncryptService("mypassword")
        hashed: str = service.password_hashed
        empty_service: EncryptService = EncryptService("")
        assert empty_service.valid_password(hashed) is False
