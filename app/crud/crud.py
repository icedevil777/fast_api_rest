"""Sync CRUD """
from fastapi import status, HTTPException
from app.schemas import BaseDelete, CreateUpdateDish, UpCrMeSub
from sqlalchemy.orm import Session
from app.models import Menu, Submenu, Dish


def get_menus(db: Session):
	"""
	Get all menus.
	:param db:
	:return:
	"""
	menus = db.query(Menu).all()
	return menus if menus else []


def get_menu(menu_id: int, db: Session):
	"""
	Get one menu.
	:param menu_id:
	:param db:
	:return:
	"""
	menu = db.query(Menu).get(menu_id)
	if menu:
		return menu
	raise HTTPException(status_code=404)


def create_menu(menu: UpCrMeSub, db: Session):
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
	db.commit()
	db.refresh(new_menu)
	return new_menu


def update_menu(menu_id: int, menu: UpCrMeSub, db: Session):
	"""
	Update one menu.
	:param menu_id:
	:param menu:
	:param db:
	:return:
	"""
	menu_to_update = get_menu(menu_id, db)
	if menu_to_update is None:
		raise HTTPException(status_code=404)
	menu_to_update.id = menu_id
	menu_to_update.title = menu.title
	menu_to_update.description = menu.description
	db.commit()
	db.refresh(menu_to_update)
	return menu_to_update


def delete_menu(menu_id: int, db: Session):
	"""
	Delete one menu.
	:param menu_id:
	:param db:
	:return:
	"""
	menu_for_delete = db.query(Menu).get(menu_id)

	if menu_for_delete is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

	db.delete(menu_for_delete)
	db.commit()
	return BaseDelete


def get_submenus(menu_id: int, db: Session):
	"""
	Get all submenus.
	:param menu_id:
	:param db:
	:return:
	"""
	submenus = db.query(Submenu).filter(
		Submenu.menu_id == menu_id).all()
	if submenus:
		return submenus
	raise HTTPException(status_code=404)


def get_submenu(
	menu_id: int,
	submenu_id: int,
	db: Session,
):
	"""
	Get one submenu.
	:param menu_id:
	:param submenu_id:
	:param db:
	:return:
	"""
	one_submenu = db.query(Submenu).filter(
		Submenu.menu_id == menu_id).filter(
		Submenu.id == submenu_id).one_or_none()

	if one_submenu is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
	else:
		return one_submenu


def create_submenu(menu_id: int, sub: UpCrMeSub, db: Session):
	"""
	Create new submenu.
	:param menu_id:
	:param sub:
	:param db:
	:return:
	"""
	new_submenu = Submenu(
		title=sub.title,
		description=sub.description,
		menu_id=menu_id,
	)
	db.add(new_submenu)
	db.commit()
	res = db.query(Submenu).filter(Submenu.menu_id == menu_id).all()
	if res is not None:
		d = db.query(Menu).filter(Menu.id == menu_id).first()
		db.add(d)
		db.commit()
	return new_submenu


def update_submenu(
	menu_id: int,
	submenu_id: int,
	submenu: UpCrMeSub,
	db: Session,
):
	"""
	Update one submenu.
	:param menu_id:
	:param submenu_id:
	:param submenu:
	:param db:
	:return:
	"""
	submenu_to_update = db.query(Submenu).filter(
		Submenu.menu_id == menu_id).filter(
		Submenu.id == submenu_id).one_or_none()
	if submenu_to_update is None:
		raise HTTPException(status_code=404)
	else:
		submenu_to_update.title = submenu.title
		submenu_to_update.description = submenu.description
		db.commit()
		db.refresh(submenu_to_update)
		return submenu_to_update


def delete_submenu(
	menu_id: int,
	submenu_id: int,
	db: Session,
):
	"""
	Delete one submenu.
	:param menu_id:
	:param submenu_id:
	:param db:
	:return:
	"""
	submenu = get_submenu(menu_id, submenu_id, db)
	if submenu is None:
		raise HTTPException(status_code=404)
	else:
		# res = db.query(Submenu).filter(Submenu.menu_id == menu_id).all()
		# d = db.query(Menu).filter(Menu.id == menu_id).first()
		db.delete(submenu)
		db.commit()
		db.commit()
		return BaseDelete


def get_dishes(
	menu_id: int,
	submenu_id: int,
	db: Session,
):
	"""
	Get all dishes.
	:param menu_id:
	:param submenu_id:
	:param db:
	:return:
	"""
	dish = db.query(Dish).filter(
		Dish.menu_id == menu_id).filter(
		Dish.submenu_id == submenu_id).all()
	return dish if dish else []


def get_dish(
	menu_id: int,
	submenu_id: int,
	dish_id: int,
	db: Session,
):
	"""
	Get one dish.
	:param menu_id:
	:param submenu_id:
	:param dish_id:
	:param db:
	:return:
	"""
	dish = db.query(Dish).join(
		Submenu, Submenu.id == Dish.submenu_id).filter(
		Dish.id == dish_id,
		Submenu.id == submenu_id,
		Submenu.menu_id == menu_id).first()
	if dish is None:
		raise HTTPException(status_code=404)
	else:
		return dish


def create_dish(
	menu_id: int,
	submenu_id: int,
	dish: CreateUpdateDish,
	db: Session,
):
	"""
	Create new dish.
	:param menu_id:
	:param submenu_id:
	:param dish:
	:param db:
	:return:
	"""
	new_dish = Dish(
		title=dish.title,
		description=dish.description,
		price=float(dish.price),
		submenu_id=submenu_id,
		menu_id=menu_id,
	)

	db_dish = db.query(Dish).filter(
		Dish.title == new_dish.title).first()
	menu = db.query(Menu).filter(Menu.id == menu_id).first()
	submenu = db.query(Submenu).filter(
		Submenu.id == submenu_id).first()
	if db_dish is not None:
		raise HTTPException(
			status_code=404,
			detail='dish already exist',
		)
	elif menu is None or submenu is None:
		raise HTTPException(
			status_code=404,
			detail='Menu or Submenu not exist',
		)
	else:
		db.add(new_dish)
		db.commit()
		count_dish_submenu = db.query(Dish).filter(
			Dish.submenu_id == submenu_id).all()
		count_dish_menu = db.query(Dish).filter(
			Dish.menu_id == menu_id).all()
		menu_dish = db.query(Menu).filter(
			Menu.id == menu_id).first()
		submenu_dish = db.query(Submenu).filter(
			Submenu.id == submenu_id).first()
		menu_dish.dishes_count = len(count_dish_menu)
		submenu_dish.dishes_count = len(count_dish_submenu)
		db.add(menu_dish)
		db.add(submenu_dish)
		db.commit()
		db.refresh(menu_dish)
		db.refresh(submenu_dish)
		return new_dish


def update_dish(
	menu_id: int,
	submenu_id: int,
	dish_id: int,
	dish: CreateUpdateDish,
	db: Session,
):
	"""
	Update one dish.
	:param menu_id:
	:param submenu_id:
	:param dish_id:
	:param dish:
	:param db:
	:return:
	"""
	dish_for_update = db.query(Dish).filter(
		Dish.id == dish_id).filter(
		Dish.menu_id == menu_id).filter(
		Dish.submenu_id == submenu_id).first()
	if dish_for_update is None:
		raise HTTPException(
			status_code=404,
			detail='Dish not found',
		)
	else:
		dish_for_update.title = dish.title
		dish_for_update.description = dish.description
		dish_for_update.price = dish.price
		db.commit()
		db.refresh(dish_for_update)
		return dish_for_update


def delete_dish(
	menu_id: int,
	submenu_id: int,
	dish_id: int,
	db: Session,
):
	"""
	Delete one dish.
	:param menu_id:
	:param submenu_id:
	:param dish_id:
	:param db:
	:return:
	"""
	dish_for_delete = get_dish(
		menu_id,
		submenu_id,
		dish_id,
		db,
	)
	if dish_for_delete is None:
		raise HTTPException(status_code=404)
	else:
		count_dish = db.query(Dish).filter(
			Dish.menu_id == menu_id).filter(
			Dish.submenu_id == submenu_id).all()
		menu_dish = db.query(Menu).filter(
			Menu.id == menu_id).first()
		submenu_dish = db.query(Submenu).filter(
			Submenu.id == submenu_id).first()
		menu_dish.dishes_count = len(count_dish) - 1
		submenu_dish.dishes_count = len(count_dish) - 1
		db.delete(dish_for_delete)
		db.commit()
		return BaseDelete
