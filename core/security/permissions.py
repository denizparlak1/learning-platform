from core.security.roles import Role

ROLE_PERMISSIONS = {
    Role.SOFTWARE_ADMIN: ["create_organization", "manage_admins", "manage_users","list_organizations","ADMIN_ACCESS"],
    Role.ORGANIZATION_ADMIN: ["update_user_status","ORG_ADMIN",
                              "create_user", "manage_organization","create_organization","content_creator","view_organization"],
    Role.NORMAL_USER: ["view_content"]
}
