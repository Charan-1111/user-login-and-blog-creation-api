from pydantic import BaseModel, Field
from typing import Optional

class RegisterUser(BaseModel):
    name: str | None = Field(default=None, examples=["user"])
    email: str | None = Field(default=None, examples=["abc@gmail.com"])
    password: str 


class LoginUser(BaseModel):
    email: str | None = Field(default= None, examples=["abc@gmail.com"])
    password: str

class ShowUser(BaseModel):
    name: str
    email: str | None = Field(default=None, examples=["abc@gmail.com"])
    
    class Config():
        from_attributes = True

class UserPassword(LoginUser):
    pass


class Blog(BaseModel):
    title: str
    content: str
    user_id: int

class ShowBlogs(BaseModel):
    title: str
    content: str