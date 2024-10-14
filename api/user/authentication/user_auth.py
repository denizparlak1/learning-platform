from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from db.mongo.connection.mongo_connection import get_database
from repository.user.auth.user_auth_repository import UserAuthRepository
from schema.user.auth.user_auth_schema import UserSigninRequest
from service.user.auth.user_auth_service import UserAuthService

router = APIRouter()

@router.post("/sign-in")
async def signin_user(data: UserSigninRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    user_repo = UserAuthRepository(db)
    user_auth_service = UserAuthService(user_repo)
    return await user_auth_service.login(data.email, data.password)
