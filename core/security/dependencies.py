from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.security.permissions import ROLE_PERMISSIONS
from functools import wraps
from core.security.security import SecurityUtils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def permission_required(required_permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: dict = Depends(get_current_active_user), **kwargs):
            role = current_user.get("role")
            if required_permission not in ROLE_PERMISSIONS.get(role, []):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Operation not permitted"
                )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator



async def get_current_active_user(token: str = Depends(oauth2_scheme)):
    try:
        return SecurityUtils.verify_token(token)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

