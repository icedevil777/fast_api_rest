"""In this module describes CRUD."""

from typing import Type
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UpCrMeSub, CreateUpdateDish, DeleteMenu, \
	DeleteSubmenu, DeleteDish, BaseSubmenu, BaseMenu, BaseDish
from app.models import Menu, Submenu, Dish
from sqlalchemy import select


async def get_menus(
	db: AsyncSession
) -> list[BaseMenu]:
	"""
	Get all menus.
	:param db:
	:return:
	"""
	menus = await db.execute(select(Menu))
	return menus.scalars().all() if menus else []


async def get_menu(
	menu_id: int,
	db: AsyncSession,
) -> BaseMenu:
	"""
	Get one menu.
	:param menu_id:
	:param db:
	:return:
	"""
	menu = await db.execute(select(Menu).where(Menu.id == menu_id))
	menu = menu.scalars().first()
	if menu is None:
		raise HTTPException(
			status_code=404,
			detail='menu not found',
		)
	return menu


async def create_menu(
	menu: UpCrMeSub,
	db: AsyncSession,
) -> BaseMenu:
	"""
	Create new menu.
	:param menu:
	:param db:
	:return:
	"""
	new_menu = Menu(
		title=menu.title,
		description=menu.description,
	)
	db.add(new_menu)
	await db.commit()
	await db.refresh(new_menu)
	return new_menu


async def update_menu(
	menu_id: int,
	menu: UpCrMeSub,
	db: AsyncSession,
) -> BaseMenu:
	"""
	Update one menu.
	:param menu_id:
	:param menu:
	:param db:
	:return:
	"""
	menu_to_update = await get_menu(
		menu_id,
		db,
	)
	if menu_to_update is None:
		raise HTTPException(status_code=404)
	menu_to_update.title = menu.title
	menu_to_update.description = menu.description
	await db.commit()
	await db.refresh(menu_to_update)
	return menu_to_update


async def delete_menu(
	menu_id: int,
	db: AsyncSession,
) -> Type[DeleteMenu]:
	"""
	Delete one menu.
	:param menu_id:
	:param db:
	:return:
	"""
	menu_for_delete = await get_menu(menu_id, db)
	if not menu_for_delete:
		raise HTTPException(status_code=404)

	await db.delete(menu_for_delete)
	await db.commit()
	return DeleteMenu


async def get_submenus(
	menu_id: int,
	db: AsyncSession,
) -> list[BaseSubmenu]:
	"""
	Get all submenus.
	:param menu_id:
	:param db:
	:return:
	"""
	# menu = await get_menu(menu_id, db)
	# if not menu:
	# 	raise HTTPException(status_code=404)
	submenus = await db.execute(select(Submenu).where(
		Submenu.menu_id == menu_id))
	return submenus.scalars().all() if submenus else []


async def get_submenu(
	menu_id: int,
	submenu_id: int,
	db: AsyncSession,
) -> BaseSubmenu:
	"""
	Get one submenu.
	:param menu_id:
	:param submenu_id:
	:param db:
	:return:
	"""
	menu = await get_menu(menu_id, db)
	if menu is None:
		raise HTTPException(status_code=404)
	submenu = await db.execute(select(
		Submenu).where(
		Submenu.menu_id == menu_id).where(
		Submenu.id == submenu_id))
	submenu = submenu.scalars().first()
	if not submenu:
		raise HTTPException(
			status_code=404,
			detail="submenu not found",
		)
	return submenu


async def create_submenu(
	menu_id: int,
	sub: UpCrMeSub,
	db: AsyncSession,
) -> BaseSubmenu:
	"""
	Create new submenu.
	:param menu_id:
	:param sub:
	:param db:
	:return:
	"""
	menu = await get_menu(menu_id, db)
	if menu is None:
		raise HTTPException(status_code=404)
	new_submenu = Submenu(
		title=sub.title,
		description=sub.description,
		menu_id=menu_id,
	)
	db.add(new_submenu)
	await db.commit()
	await db.refresh(new_submenu)
	return new_submenu


async def update_submenu(
	menu_id: int,
	submenu_id: int,
	submenu: UpCrMeSub,
	db: AsyncSession,
) -> BaseSubmenu:
	"""
	Update one submenu.
	:param menu_id:
	:param submenu_id:
	:param submenu:
	:param db:
	:return:
	"""
	submenu_to_update = await get_submenu(
		menu_id=menu_id,
		submenu_id=submenu_id,
		db=db
	)
	if submenu_to_update is None:
		raise HTTPException(status_code=404)
	submenu_to_update.title = submenu.title
	submenu_to_update.description = submenu.description
	db.add(submenu_to_update)
	await db.commit()
	await db.refresh(submenu_to_update)
	return submenu_to_update


async def delete_submenu(
	menu_id: int,
	submenu_id: int,
	db: AsyncSession,
) -> Type[DeleteSubmenu]:
	"""
	Delete one submenu.
	:param menu_id:
	:param submenu_id:
	:param db:
	:return:
	"""
	submenu = await get_submenu(
		menu_id=menu_id,
		submenu_id=submenu_id,
		db=db,
	)
	if submenu is None:
		raise HTTPException(status_code=404)
	await db.delete(submenu)
	await db.commit()
	return DeleteSubmenu


async def get_dishes(
	menu_id: int,
	submenu_id: int,
	db: AsyncSession,
) -> list[BaseDish]:
	"""
	Get all dishes."
	:param menu_id: 
	:param submenu_id: 
	:param db: 
	:return: 
	"""""
	# menu = await get_menu(menu_id, db)
	# submenu = await get_submenu(menu_id, submenu_id, db)
	# if menu is None:
	# 	raise HTTPException(
	# 		status_code=404,
	# 		detail='menu not found'
	# 	)
	# if submenu is None:
	# 	raise HTTPException(
	# 		status_code=404,
	# 		detail='submenu not found'
	# 	)

	dishes = await db.execute(select(Dish).where(
		Dish.menu_id == menu_id).where(
		Dish.submenu_id == submenu_id))
	return dishes.scalars().all() if dishes else []


async def get_dish(
	menu_id: int,
	submenu_id: int,
	dish_id: int,
	db: AsyncSession,
) -> BaseDish:
	"""
	Get one dish.
	:param menu_id:
	:param submenu_id:
	:param dish_id:
	:param db:
	:return:
	"""
	menu = await get_menu(menu_id, db)
	submenu = await get_submenu(
		menu_id=menu_id,
		submenu_id=submenu_id,
		db=db,
	)
	if menu is None or submenu is None:
		raise HTTPException(status_code=404)
	dish = await db.execute(select(Dish).where(
		Dish.menu_id == menu_id).where(
		Dish.submenu_id == submenu_id).where(
		Dish.id == dish_id))
	dish = dish.scalars().first()
	if dish is None:
		raise HTTPException(
			status_code=404,
			detail="dish not found",
		)
	return dish


async def create_dish(
	menu_id: int,
	submenu_id: int,
	dish: CreateUpdateDish,
	db: AsyncSession,
) -> BaseDish:
	"""
	Create new dish.
	:param menu_id:
	:param submenu_id:
	:param dish:
	:param db:
	:return:
	"""
	menu = await get_menu(menu_id, db)
	submenu = await get_submenu(menu_id, submenu_id, db)
	if menu is None or submenu is None:
		raise HTTPException(status_code=404)
	print('dish.price', dish.price)
	# try:
	# 	price = str(round(float(dish.price), 2))
	# 	print("price", price, type(price))
	# except:
	# 	raise HTTPException(status_code=415)
	new_dish = Dish(
		title=dish.title,
		description=dish.description,
		price=dish.price,
		submenu_id=submenu_id,
		menu_id=menu_id,
	)

	db.add(new_dish)
	await db.commit()
	await db.refresh(new_dish)
	return new_dish


async def update_dish(
	menu_id: int,
	submenu_id: int,
	dish_id: int,
	dish: CreateUpdateDish,
	db: AsyncSession
) -> BaseDish:
	"""
	Update one dish.
	:param menu_id:
	:param submenu_id:
	:param dish_id:
	:param dish:
	:param db:
	:return:
	"""
	menu = await get_menu(menu_id, db)
	submenu = await get_submenu(menu_id, submenu_id, db)
	if menu is None or submenu is None:
		raise HTTPException(status_code=404)
	dish_for_update = await get_dish(
		menu_id=menu_id,
		submenu_id=submenu_id,
		dish_id=dish_id,
		db=db,
	)
	if dish_for_update is None:
		raise HTTPException(status_code=404)
	price = str(round(float(dish.price), 2))
	dish_for_update.title = dish.title
	dish_for_update.description = dish.description
	dish_for_update.price = price
	await db.commit()
	await db.refresh(dish_for_update)
	return dish_for_update


async def delete_dish(
	menu_id: int,
	submenu_id: int,
	dish_id: int,
	db: AsyncSession,
) -> Type[DeleteDish]:
	"""
	Delete one dish.
	:param menu_id:
	:param submenu_id:
	:param dish_id:
	:param db:
	:return:
	"""
	dish_for_delete = await get_dish(
		menu_id=menu_id,
		submenu_id=submenu_id,
		dish_id=dish_id,
		db=db,
	)
	if dish_for_delete is None:
		raise HTTPException(status_code=404)
	await db.delete(dish_for_delete)
	await db.commit()
	return DeleteDish
