from pydantic import BaseModel
from typing import Optional


class PostModel(BaseModel):
    id: Optional[int] = None
    userId: int
    title: str
    body: str


class CreatePostModel(BaseModel):
    userId: int
    title: str
    body: str