from pydantic import BaseModel, EmailStr


class UserSigninRequest(BaseModel):
    email: EmailStr
    password: str