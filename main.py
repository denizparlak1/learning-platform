from fastapi import FastAPI
from api.admin.authentication import admin_auth
from  db.mongo.connection.mongo_connection import  get_database

app = FastAPI()

app.include_router(admin_auth.router, prefix="/api/admin/authentication",tags=["Admin Authentication"])