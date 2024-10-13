from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from core.security.dependencies import permission_required, get_current_active_user
from db.mongo.connection.mongo_connection import get_database
from repository.organization.organization_repository import OrganizationRepository, OrganizationAuthRepository
from schema.organization.auth.organization_auth_schema import OrganizationInfo, OrganizationAdminCreate, \
    OrganizationLoginSchema
from service.organization.auth.organization_auth_service import OrganizationAuthService

router = APIRouter()

@router.post("/sign-up/")
@permission_required("create_organization")
async def create_organization_api(
    organization_info: OrganizationInfo,
    admin_info: OrganizationAdminCreate,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    org_repo = OrganizationRepository(db)
    admin_repo = OrganizationAuthRepository(db)
    service = OrganizationAuthService(org_repo, admin_repo)
    result = await service.create_organization_and_admin(organization_info, admin_info)

    return {"organization_id": result["organization_id"]}

@router.post("/sign-in")
async def login_organization_user(
    login_data: OrganizationLoginSchema,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    org_repo = OrganizationRepository(db)
    admin_repo = OrganizationAuthRepository(db)
    service = OrganizationAuthService(org_repo, admin_repo)
    result = await service.login_organization_user(login_data.email, login_data.password)
    return result