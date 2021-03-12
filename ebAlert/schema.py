from . import createLogger

log = createLogger(__name__)

try:
    from pydantic import BaseModel
except ImportError as e:
    log.error("pydantic package is required\n pip install pydantic")

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