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
