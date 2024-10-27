from fastapi import FastAPI
from api.admin.authentication import admin_auth
from api.admin.organization import admin_organization_route
from api.organization.authentication import organization_auth
from api.organization.content import content_route
from api.organization.info import organization_info_route
from api.user.authentication import user_auth
app = FastAPI()

app.include_router(admin_auth.router, prefix="/api/admin/authentication",tags=["Admin Authentication"])
app.include_router(organization_auth.router, prefix="/api/organization/authentication",tags=["Organization Authentication"])
app.include_router(user_auth.router, prefix="/api/user/authentication",tags=["User Authentication"])
app.include_router(organization_info_route.router, prefix="/api/organization/organization",tags=["Organization Info"])

app.include_router(content_route.router, prefix="/api/organization/content",tags=["Organization Contents"])
app.include_router(admin_organization_route.router, prefix="/api/admin/organization",tags=["Admin Organization Info"])