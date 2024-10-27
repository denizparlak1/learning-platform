from fastapi import APIRouter, Depends, Header
from motor.motor_asyncio import AsyncIOMotorDatabase

from core.security.dependencies import get_current_active_user
from db.mongo.async_connection.connection.mongo_connection import get_database
from schema.admin.auth.admin_auth_schema import SignupRequest, SigninRequest, ResetPasswordRequest, \
    UpdateAdminPasswordRequest
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

@router.post("/reset-password")
async def reset_admin_password(
    request: ResetPasswordRequest,
    access_key: str = Header(...),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Endpoint for resetting the password of a software admin.
    Requires the special access key in the header for security.
    """
    admin_auth_service = AdminAuthService(db)
    return await admin_auth_service.reset_password(email=request.email, access_key=access_key)

@router.put("/update-password")
async def update_admin_password(
    request: UpdateAdminPasswordRequest,
    access_key: str = Header(...),
    current_user: dict = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Endpoint for updating the password of a software admin.
    Requires the current password and the new password in the JSON body.
    Also requires the special access key in the header for security.
    """
    admin_auth_service = AdminAuthService(db)
    return await admin_auth_service.update_password(
        email=current_user["email"],
        current_password=request.current_password,
        new_password=request.new_password
    )