import hashlib
from settings import COMMON_PASSWORD


class PasswordUtil():
    @classmethod
    def make_hex(cls, password) -> str:
        password_byte = bytes(password, 'utf-8')
        return hashlib.sha256(password_byte).hexdigest()

    @classmethod
    def is_same(cls, password, password_hex) -> bool:
        return cls.make_hex(password) == password_hex

    @classmethod
    def is_correct_common_password(cls, common_password) -> bool:
        return common_password == COMMON_PASSWORD
