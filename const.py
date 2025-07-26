from enum import Enum, unique


@unique
class UserStatus(Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"

    @classmethod
    def has(cls, target):
        for name in cls.__members__:
            if name == target:
                return True

        return False


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


ROLE_ADMIN = "admin"
ROLE_SUPER_ADMIN = "super_admin"


@unique
class RoleStatus(Enum):
    active = "active"


SESSION_KEY_REGISTER_VERIFICATION_CODE = "__register_verification_code__"
SESSION_KEY_REGISTER_VERIFICATION_EMAIL = "__register_verification_email__"
SESSION_KEY_REGISTER_VERIFICATION_TIMESTAMP = "__register_verification_ts__"

SESSION_KEY_CHANGE_PASSWORD_VERIFICATION_NAME = "__change_password_verification_name__"  # noqa
SESSION_KEY_CHANGE_PASSWORD_VERIFICATION_CODE = "__change_password_verification_code__"  # noqa
SESSION_KEY_CHANGE_PASSWORD_VERIFICATION_EMAIL = "__change_password_verification_email__"  # noqa
SESSION_KEY_CHANGE_PASSWORD_VERIFICATION_TIMESTAMP = "__change_password_verification_timestamp__"  # noqa
