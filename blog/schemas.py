from pydantic import BaseModel
from typing import Optional, List


class BlogBase(BaseModel):
    title: str
    body: str
    published: Optional[bool]


class Blog(BlogBase):
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class ShowUserWithBlogs(ShowUser):
    blogs: List[Blog] = []


class DisplayBlog(BaseModel):
    title: str
    body: str
    author: ShowUser

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None