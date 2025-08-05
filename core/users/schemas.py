from pydantic import BaseModel,Field,field_validator,EmailStr
from typing import Optional
from datetime import datetime


class UserLoginSchema(BaseModel):
    username : str = Field(...,max_length=259,description="username of the user")
    password : str = Field(...,description="password of the user")
    
class UserRegisterSchema(BaseModel):
    username : str = Field(...,max_length=259,description="username of the user")
    password : str = Field(...,description="password of the user")
    password_confirm : str = Field(...,description="confirm password of the user")
    
    @field_validator("password_confirm")
    def check_passwords_match(cls,password_confirm,validation):
        if not(password_confirm == validation.data.get("password")):
            raise ValueError("password doesnt match")
        return password_confirm
    
class UserRefreshTokenSchema(BaseModel):
    token: str = Field(..., description="refresh token of the user")