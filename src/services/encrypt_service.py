from werkzeug.security import check_password_hash, generate_password_hash


class EncryptService:
    def __init__(self, password: str) -> None:
        self.__password = password

    @property
    def password(self) -> str:
        return self.__password

    @property
    def password_hashed(self) -> str:
        return generate_password_hash(self.password)

    def valid_password(self, pwhash: str) -> bool:
        return check_password_hash(pwhash, self.password)
