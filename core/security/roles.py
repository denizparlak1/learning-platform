from enum import Enum

class Role(str, Enum):
    SOFTWARE_ADMIN = "software_admin"
    ORGANIZATION_ADMIN = "organization_admin"
    NORMAL_USER = "normal_user"
