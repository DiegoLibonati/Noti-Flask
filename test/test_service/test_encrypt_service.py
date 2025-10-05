from src.services.encrypt_service import EncryptService


def test_initialize_encrypt_service() -> None:
    service: EncryptService = EncryptService("plain_password")

    assert isinstance(service, EncryptService)
    assert service.password == "plain_password"


def test_password_hashed_is_different() -> None:
    service: EncryptService = EncryptService("secure123")
    hashed: str = service.password_hashed

    assert isinstance(hashed, str)
    assert hashed != service.password
    assert any(hashed.startswith(prefix) for prefix in ("pbkdf2:", "scrypt:"))


def test_valid_password_returns_true() -> None:
    service: EncryptService = EncryptService("mypassword")
    hashed: str = service.password_hashed

    is_valid: bool = service.valid_password(hashed)

    assert is_valid is True


def test_valid_password_returns_false() -> None:
    correct_service: EncryptService = EncryptService("rightpass")
    wrong_service: EncryptService = EncryptService("wrongpass")

    hashed: str = correct_service.password_hashed
    is_valid: bool = wrong_service.valid_password(hashed)

    assert is_valid is False
