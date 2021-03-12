from pydantic import BaseModel


class Link(BaseModel):
    id: int
    link: str

    class Config:
        orm_mode = True


class Post(BaseModel):
    id: int
    title: str
    price: str
    post_id: int
    link: str

    class Config:
        orm_mode = True