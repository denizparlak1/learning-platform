from pydantic import BaseModel

class AdminOrganizationUserCount(BaseModel):
    organization_id: str
    total_users: int