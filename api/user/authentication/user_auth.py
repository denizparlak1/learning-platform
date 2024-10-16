from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from core.security.dependencies import get_current_active_user
from db.mongo.connection.mongo_connection import get_database
from mail.service.postmark_service import PostmarkService, get_postmark_service
from repository.user.auth.user_auth_repository import UserAuthRepository
from schema.user.auth.user_auth_schema import UserSigninRequest, ResetPasswordRequest, UpdatePasswordRequest
from service.user.auth.user_auth_service import UserAuthService

router = APIRouter()

@router.post("/sign-in")
async def signin_user(data: UserSigninRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    user_repo = UserAuthRepository(db)
    user_auth_service = UserAuthService(user_repo)
    return await user_auth_service.login(data.email, data.password)


@router.post("/reset-password/")
async def reset_password(
    request: ResetPasswordRequest,
    db: AsyncIOMotorDatabase = Depends(get_database),
    email_service: PostmarkService = Depends(get_postmark_service)
):
    user_repo = UserAuthRepository(db)
    user_auth_service = UserAuthService(user_repo)

    return await user_auth_service.reset_password(request.email, email_service)


@router.put("/update-password")
async def update_password(
        update_data: UpdatePasswordRequest,
        current_user: dict = Depends(get_current_active_user),
        db: AsyncIOMotorDatabase = Depends(get_database)
):
    user_repo = UserAuthRepository(db)
    user_auth_service = UserAuthService(user_repo)

    return await user_auth_service.update_password(
        user_id=current_user["_id"],
        current_password=update_data.current_password,
        new_password=update_data.new_password
    )