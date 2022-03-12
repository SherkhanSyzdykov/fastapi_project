from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class AbstractBaseModel(BaseModel):
    class Config:
        orm_mode = True


class Url(AbstractBaseModel):
    id: int
    url: str


class Urls(AbstractBaseModel):
    items: List[Url] = []


class Request(AbstractBaseModel):
    id: int
    body: Dict[str, Any]
    key: Optional[str]


class Requests(AbstractBaseModel):
    items: List[Request] = []
