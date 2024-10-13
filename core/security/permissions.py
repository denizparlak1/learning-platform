from core.security.roles import Role

ROLE_PERMISSIONS = {
    Role.SOFTWARE_ADMIN: ["create_organization", "manage_admins", "manage_users"],
    Role.ORGANIZATION_ADMIN: ["create_user", "manage_organization","create_organization"],
    Role.NORMAL_USER: ["view_content"]
}
