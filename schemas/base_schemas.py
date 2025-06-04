from pydantic import BaseModel,EmailStr


class User(BaseModel):
    id: int
    name: str
    is_active: bool
    email: EmailStr

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserOutputSchemas(BaseModel):
    message: str
    user: User

class UpdateUser(UserCreate):
    pass