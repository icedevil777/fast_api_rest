from typing import Type
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession

import async_crud
from database import AsyncSessionLocal, SessionLocal, get_async_db
from schemas import BaseMenu, BaseDish, BaseSubmenu, UpCrMeSub,\
	CreateUpdateDish, DeleteMenu, DeleteSubmenu, DeleteDish
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings import settings

app = FastAPI(title=settings.app_title)

app.add_middleware(
	CORSMiddleware,
	allow_credentials=True,
	allow_headers=['*'],
	allow_methods=['*'],
)


@app.get("/")
async def root():
	"""
	Hello Ylab
	:return: dict
	"""
	return {"msg": "Hello Ylab"}


@app.get(
	"/api/v1/menus",
	response_model=list[BaseMenu],
	summary='Get List of Menus',
	description="Getting all list of menus",
	status_code=200
)
async def get_menus(
	db: AsyncSession = Depends(get_async_db),
) -> list[BaseMenu]:
	"""
	Get all menus.
	:param db:
	:return:
	"""
	return await async_crud.get_menus(db)


@app.get(
	"/api/v1/menus/{menu_id}",
	response_model=BaseMenu,
)
async def get_menu(
	menu_id: int,
	db: AsyncSession = Depends(get_async_db)
) -> BaseMenu:
	"""
	Get one menu  by id.
	:param menu_id:
	:param db:
	:return:
	"""
	return await async_crud.get_menu(menu_id, db)


@app.post(
	"/api/v1/menus",
	response_model=BaseMenu,
	status_code=201
)
async def create_menu(
	menu: UpCrMeSub,
	db: AsyncSession = Depends(get_async_db)
) -> BaseMenu:
	"""
	Create new menu.
	:param menu:
	:param db:
	:return:
	"""
	return await async_crud.create_menu(menu, db)


@app.patch(
	"/api/v1/menus/{menu_id}",
	response_model=BaseMenu,
	status_code=200
)
async def update_menu(
	menu_id: int,
	menu: UpCrMeSub,
	db: AsyncSession = Depends(get_async_db)
) -> BaseMenu:
	"""
	Update one menu.
	:param menu_id:
	:param menu:
	:param db:
	:return:
	"""
	return await async_crud.update_menu(
		menu_id,
		menu,
		db
	)


@app.delete(
	"/api/v1/menus/{menu_id}",
	response_model=DeleteMenu,
	status_code=200
)
async def delete_menu(
	menu_id: int,
	db: AsyncSession = Depends(get_async_db)
) -> Type[DeleteMenu]:
	"""
	Delete_menu some menu by id.
	:param menu_id:
	:param db:
	:return:
	"""
	return await async_crud.delete_menu(menu_id, db)


@app.get(
	"/api/v1/menus/{menu_id}/submenus",
	response_model=list[BaseSubmenu],
	status_code=200,
)
async def get_submenus(
	menu_id: int,
	db: AsyncSession = Depends(get_async_db)
) -> list[BaseSubmenu]:
	"""
	Get all submenus by menu id.
	:param menu_id:
	:param db:
	:return:
	"""
	return await async_crud.get_submenus(
		menu_id,
		db
	)


@app.post(
	"/api/v1/menus/{menu_id}/submenus",
	response_model=BaseSubmenu,
	status_code=201
)
async def create_submenu(
	menu_id: int,
	sub: UpCrMeSub,
	db: AsyncSession = Depends(get_async_db)
) -> BaseSubmenu:
	"""
	Create new submenu in menu.
	:param menu_id:
	:param sub:
	:param db:
	:return:
	"""
	return await async_crud.create_submenu(
		menu_id,
		sub,
		db
	)


@app.get(
	"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
	response_model=BaseSubmenu,
	status_code=200)
async def get_submenu(
	menu_id: int,
	submenu_id: int,
	db: AsyncSession = Depends(get_async_db)
) -> BaseSubmenu:
	"""
	Get one submenu by two id.
	:param menu_id:
	:param submenu_id:
	:param db:
	:return:
	"""
	return await async_crud.get_submenu(
		menu_id,
		submenu_id,
		db
	)


@app.patch(
	"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
	response_model=BaseSubmenu,
	status_code=200,
)
async def update_submenu(
	menu_id: int,
	submenu_id: int,
	sub: UpCrMeSub,
	db: AsyncSession = Depends(get_async_db)
) -> BaseSubmenu:
	"""
	Update one submenu by menu id.
	:param menu_id:
	:param submenu_id:
	:param sub:
	:param db:
	:return:
	"""
	return await async_crud.update_submenu(
		menu_id=menu_id,
		submenu_id=submenu_id,
		submenu=sub,
		db=db,
	)


@app.delete(
	"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
	response_model=DeleteSubmenu,
	status_code=200,
)
async def delete_submenu(
	menu_id: int,
	submenu_id: int,
	db: AsyncSession = Depends(get_async_db)
) -> Type[DeleteSubmenu]:
	"""
	Delete one submenu by menu id.
	:param menu_id:
	:param submenu_id:
	:param db:
	:return:
	"""
	return await async_crud.delete_submenu(
		menu_id=menu_id,
		submenu_id=submenu_id,
		db=db,
	)


@app.get(
	"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
	response_model=list[BaseDish],
	status_code=200,
)
async def get_dishes(
	menu_id: int,
	submenu_id: int,
	db: AsyncSession = Depends(get_async_db)
) -> list[BaseDish]:
	"""
	Get all dishes by menu and submenu id.
	:param menu_id:
	:param submenu_id:
	:param db:
	:return:
	"""
	return await async_crud.get_dishes(
		menu_id=menu_id,
		submenu_id=submenu_id,
		db=db
	)


@app.post(
	"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
	response_model=BaseDish,
	status_code=201,
)
async def create_dish(
	menu_id: int,
	submenu_id: int,
	dish: CreateUpdateDish,
	db: AsyncSession = Depends(get_async_db)
) -> BaseDish:
	"""
	Create new dish.
	:param menu_id:
	:param submenu_id:
	:param dish:
	:param db:
	:return:
	"""
	return await async_crud.create_dish(
		menu_id=menu_id,
		submenu_id=submenu_id,
		dish=dish,
		db=db,
	)


@app.get(
	"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
	response_model=BaseDish,
	status_code=200,
)
async def get_dish(
	menu_id: int,
	submenu_id: int,
	dish_id: int,
	db: AsyncSession = Depends(get_async_db)
) -> BaseDish:
	"""
	Get some dish by id.
	:param menu_id:
	:param submenu_id:
	:param dish_id:
	:param db:
	:return:
	"""
	return await async_crud.get_dish(
		menu_id,
		submenu_id,
		dish_id,
		db
	)


@app.patch(
	"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
	response_model=BaseDish,
	status_code=200,
)
async def update_dish(
	menu_id: int,
	submenu_id: int,
	dish_id: int,
	dish: CreateUpdateDish,
	db: AsyncSession = Depends(get_async_db)
) -> BaseDish:
	"""
	Update one dish by id.
	:param menu_id:
	:param submenu_id:
	:param dish_id:
	:param dish:
	:param db:
	:return:
	"""
	return await async_crud.update_dish(
		menu_id,
		submenu_id,
		dish_id,
		dish,
		db
	)


@app.delete(
	"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
	response_model=DeleteDish,
	status_code=200
)
async def delete_dish(
	menu_id: int,
	submenu_id: int,
	dish_id: int,
	db: AsyncSession = Depends(get_async_db)
) -> Type[DeleteDish]:
	"""
	Delete some dish by id.
	:param menu_id:
	:param submenu_id:
	:param dish_id:
	:param db:
	:return:
	"""
	return await async_crud.delete_dish(
		menu_id=menu_id,
		submenu_id=submenu_id,
		dish_id=dish_id,
		db=db,
	)


if __name__ == '__main__':
	uvicorn.run(
		'main:app',
		port=8000,
		host='0.0.0.0',
		reload=True
	)
