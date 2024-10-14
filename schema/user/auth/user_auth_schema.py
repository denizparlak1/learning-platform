from pydantic import BaseModel, EmailStr


class UserSigninRequest(BaseModel):
    email: EmailStr
    password: str

class ResetPasswordRequest(BaseModel):
    email: EmailStr

class UpdatePasswordRequest(BaseModel):
    current_password: str
    new_password: str
