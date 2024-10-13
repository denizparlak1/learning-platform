from fastapi import FastAPI
from api.admin.authentication import admin_auth
from api.organization.authentication import organization_auth
from  db.mongo.connection.mongo_connection import  get_database

app = FastAPI()

app.include_router(admin_auth.router, prefix="/api/admin/authentication",tags=["Admin Authentication"])
app.include_router(organization_auth.router, prefix="/api/organization/authentication",tags=["Organization Authentication"])