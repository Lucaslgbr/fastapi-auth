from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    fullname: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "André Cristen",
                "email": "admin@admin.com",
                "password": "teste"
            }
        }

class User(UserBase):
    id: int


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@admin.com",
                "password": "teste"
            }
        }
