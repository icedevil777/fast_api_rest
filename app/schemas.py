from typing import Optional
from pydantic import BaseModel


class BaseMenu(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    # dishes_count: Optional[int]
    # submenus_count: Optional[int]

    class Config:
        orm_mode = True


class CreateMenu(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class BaseDelete(BaseModel):
    status: bool = True
    massage: str = "It's deleted"

    class Config:
        orm_mode = True


class BaseSubmenu(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    # dishes_count: Optional[int]

    class Config:
        orm_mode = True


class BaseDish(BaseModel):
    id: int
    title: Optional[str]
    price: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True


class PatchMenu(BaseMenu):
    id: int
    title: Optional[str]
    description: Optional[str]
    # dishes_count: Optional[int]


class PatchSubmenu(BaseSubmenu):
    title: Optional[str]
    description: Optional[str]


class UpgradeDish(BaseDish):
    title: str
    description: str
    price: float
