from typing import Optional
from pydantic import BaseModel


class BaseMenu(BaseModel):
    id: str = "menu_id (str)"
    title: Optional[str] = "menu title (str)"
    description: Optional[str] = "menu description (str)"
    dishes_count: Optional[int] = 0
    submenus_count: Optional[int] = 0

    class Config:
        orm_mode = True


class BaseSubmenu(BaseModel):
    id: str = "submenu_id (str)"
    title: Optional[str] = "submenu title (str)"
    description: Optional[str] = "submenu description (str)"
    dishes_count: Optional[int] = 0

    class Config:
        orm_mode = True


class BaseDish(BaseModel):
    id: str = "dish_id (str)"
    title: Optional[str] = "dish title (str)"
    description: Optional[str] = "dish description (str)"
    price: Optional[str] = "0.00"

    class Config:
        orm_mode = True


class UpCrMeSub(BaseModel):
    title: str = "title"
    description: str = "description"


class CreateUpdateDish(BaseModel):
    title: Optional[str] = "dish title"
    description: Optional[str] = "dish description"
    price: Optional[str] = "0.00"

    class Config:
        orm_mode = True


class BaseDelete(BaseModel):
    status: bool = True

    class Config:
        orm_mode = True


class DeleteMenu(BaseDelete):
    message: str = "The menu has been deleted"


class DeleteSubmenu(BaseDelete):
    message: str = "The submenu has been deleted"


class DeleteDish(BaseDelete):
    message: str = "The dish has been deleted"


