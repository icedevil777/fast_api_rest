from typing import Optional
from pydantic import BaseModel


class BaseMenu(BaseModel):
    id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    dishes_count: Optional[int]
    submenus_count: Optional[int]

    class Config:
        orm_mode = True


class BaseSubmenu(BaseModel):
    id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    dishes_count: Optional[int]

    class Config:
        orm_mode = True


class BaseDish(BaseModel):
    id: Optional[int]
    title: Optional[str]
    price: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True


#Удалить ?
class PatchMenu(BaseMenu):
    id: Optional[int]
    title: str
    description: str
    dishes_count: Optional[int]



class PatchSubmenu(BaseSubmenu):
    title: Optional[str]
    description: Optional[str]


#Удалить ?
class UpgradeDish(BaseDish):
    title: str
    description: str
    price: float
