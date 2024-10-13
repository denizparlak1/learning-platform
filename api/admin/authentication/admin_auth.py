from fastapi import APIRouter, Depends, Header
from motor.motor_asyncio import AsyncIOMotorDatabase
from db.mongo.connection.mongo_connection import get_database
from schema.admin.auth.admin_auth_schema import SignupRequest, SigninRequest
from service.admin.auth.admin_auth_service import AdminAuthService

router = APIRouter()


@router.post("/sign-up")
async def signup(data: SignupRequest, db: AsyncIOMotorDatabase = Depends(get_database),access_key: str = Header(...)):
    admin_service = AdminAuthService(db)
    return await admin_service.signup(data.name, data.email, data.password,access_key)

@router.post("/sign-in")
async def signin(data: SigninRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    admin_service = AdminAuthService(db)
    return await admin_service.signin(data.email, data.password)