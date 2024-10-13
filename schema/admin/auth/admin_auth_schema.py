from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class SigninRequest(BaseModel):
    email: EmailStr
    password: str