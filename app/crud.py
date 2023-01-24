import os
from fastapi import FastAPI, status, HTTPException
from app.schemas import BaseMenu, BaseSubmenu, PatchMenu, BaseDish, PatchSubmenu
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.models import Menu, Submenu, Dish


def get_menus(db: Session):
    """Get all menus"""
    menus = db.query(Menu).all()
    return menus if menus else []


def get_menu(db: Session, menu_id: int):
    """Get one menu"""
    menu = db.query(Menu).filter(Menu.id == menu_id).one_or_none()
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return menu



def create_menu(db: Session, menu: BaseMenu):
    """Create new menu"""
    res = db.query(Submenu).filter(Submenu.menu_id == menu.id).all()
    new_menu = Menu(
        id=(menu.id or 0),
        title=menu.title,
        description=menu.description,
        submenus_count=len(res)
    )
    db.add(new_menu)
    db.commit()
    return new_menu


def update_menu(db: Session, menu_id: int, menu: BaseMenu):
    """Update one menu"""
    menu_to_update = db.query(Menu).filter(Menu.id == menu_id).one_or_none()
    if menu_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    menu_to_update.id = menu_id
    menu_to_update.title = menu.title
    menu_to_update.description = menu.description
    db.commit()
    db.refresh(menu_to_update)
    return menu_to_update


def delete_menu(db: Session, menu_id: int):
    """Delete one menu"""
    menu_for_delete = db.query(Menu).get(menu_id)
    if menu_for_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        db.delete(menu_for_delete)
        db.commit()
        return {
            "status": True,
            "message": "The menu has been deleted"
        }


def get_submenus(db: Session, menu_id: int):
    """Get all submenus"""
    submenus = db.query(Submenu).filter(
        Submenu.menu_id == menu_id).all()
    return submenus if submenus else []


def get_submenu(db: Session, menu_id: int, submenu_id: int):
    """Get one submenu"""
    one_submenu = db.query(Submenu).filter(
        Submenu.menu_id == menu_id).filter(
        Submenu.id == submenu_id).one_or_none()

    if one_submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return one_submenu


def create_submenu(db: Session, menu_id: int, sub: BaseSubmenu):
    """Create new submenu"""
    new_submenu = Submenu(
        id=(sub.id or 0),
        title=sub.title,
        description=sub.description,
        menu_id=menu_id
    )
    db.add(new_submenu)
    db.commit()
    res = db.query(Submenu).filter(Submenu.menu_id == menu_id).all()
    if res is not None:
        d = db.query(Menu).filter(Menu.id == menu_id).first()
        d.submenus_count = len(res)
        db.add(d)
        db.commit()
    return new_submenu


def update_submenu(db: Session, menu_id: int, submenu_id: int, submenu: PatchSubmenu):
    """Update one submenu"""
    submenu_to_update = db.query(Submenu).filter(
        Submenu.menu_id == menu_id).filter(
        Submenu.id == submenu_id).one_or_none()
    if submenu_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        submenu_to_update.title = submenu.title
        submenu_to_update.description = submenu.description
        db.commit()
        db.refresh(submenu_to_update)
        return submenu_to_update


def delete_submenu(db: Session, menu_id: int, submenu_id: int):
    """Delete one submenu"""
    submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    if submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        res = db.query(Submenu).filter(Submenu.menu_id == menu_id).all()
        d = db.query(Menu).filter(Menu.id == menu_id).first()
        d.submenus_count = len(res) - 1
        db.delete(submenu)
        db.commit()
        db.refresh(d)
        count_dish_for_this_menu = db.query(Dish).filter(Dish.menu_id == menu_id).all()
        d.dishes_count = len(count_dish_for_this_menu)
        db.commit()
        db.refresh(d)
        return {
            "status": True,
            "message": "Submenu's been deleted"
        }


def get_dishes(db: Session, menu_id: int, submenu_id: int):
    """Get all dishes"""
    dish = db.query(Dish).filter(
        Dish.menu_id == menu_id).filter(
        Dish.submenu_id == submenu_id).all()
    return dish if dish else []


def get_dish(db: Session, menu_id: int, submenu_id: int, dish_id: int):
    """Get one dish"""
    dish = db.query(Dish).join(Submenu, Submenu.id == Dish.submenu_id).filter(
        Dish.id == dish_id,
        Submenu.id == submenu_id,
        Submenu.menu_id == menu_id).first()
    if dish is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return dish


def create_dish(db: Session, menu_id: int, submenu_id: int, dish: BaseDish):
    """Create new dish"""
    new_dish = Dish(
        id=(dish.id or 0),
        title=dish.title,
        description=dish.description,
        price=float(dish.price),
        submenu_id=submenu_id,
        menu_id=menu_id,
    )

    db_dish = db.query(Dish).filter(Dish.title == new_dish.title).first()
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    if db_dish is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='dish already exist')
    elif menu is None or submenu is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Menu or Submenu not exist'
        )
    else:
        db.add(new_dish)
        db.commit()
        count_dish_submenu = db.query(Dish).filter(Dish.submenu_id == submenu_id).all()
        count_dish_menu = db.query(Dish).filter(Dish.menu_id == menu_id).all()
        menu_dish = db.query(Menu).filter(Menu.id == menu_id).first()
        submenu_dish = db.query(Submenu).filter(Submenu.id == submenu_id).first()
        menu_dish.dishes_count = len(count_dish_menu)
        submenu_dish.dishes_count = len(count_dish_submenu)
        db.add(menu_dish)
        db.add(submenu_dish)
        db.commit()
        db.refresh(menu_dish)
        db.refresh(submenu_dish)
        return new_dish


def update_dish(db: Session, menu_id: int, submenu_id: int, dish_id: int, dish: BaseDish):
    """Update one dish"""
    dish_for_update = db.query(Dish).filter(Dish.id == dish_id).filter(
        Dish.menu_id == menu_id).filter(Dish.submenu_id == submenu_id).first()
    if dish_for_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Dish not found')
    else:
        dish_for_update.title = dish.title
        dish_for_update.description = dish.description
        dish_for_update.price = dish.price
        db.commit()
        db.refresh(dish_for_update)
        return dish_for_update


def delete_dish(db: Session, menu_id: int, submenu_id: int, dish_id: int):
    """Delete one dish"""
    dish_for_delete = db.query(Dish).filter(Dish.id == dish_id).filter(
        Dish.menu_id == menu_id).filter(Dish.submenu_id == submenu_id).first()
    if dish_for_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        count_dish = db.query(Dish).filter(Dish.menu_id == menu_id).filter(
            Dish.submenu_id == submenu_id).all()
        menu_dish = db.query(Menu).filter(Menu.id == menu_id).first()
        submenu_dish = db.query(Submenu).filter(Submenu.id == submenu_id).first()
        menu_dish.dishes_count = len(count_dish) - 1
        submenu_dish.dishes_count = len(count_dish) - 1
        db.delete(dish_for_delete)
        db.commit()
        return {
            "status": True,
            "message": "The dish has been deleted"
        }
