from pydantic import BaseModel


class Bot(BaseModel):
    id: int
    token: str
    chat_id: int
    comment: str

    class Config:
        orm_mode = True


class Link(BaseModel):
    id: int
    link: str
    bot: Bot

    class Config:
        orm_mode = True

