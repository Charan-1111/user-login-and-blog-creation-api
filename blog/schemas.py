from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
    title : str
    body : str

class UpdateBlog(BaseModel):
    title: Optional[str]
    body: Optional[str]


class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser
    class Config():
        from_attributes = True 