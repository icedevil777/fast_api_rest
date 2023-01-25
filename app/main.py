import uvicorn
from starlette import status
from . import crud
from app import models
from app.database import engine
from app.models import Menu, Submenu, Dish
from app.schemas import BaseMenu, BaseDelete, BaseDish, BaseSubmenu, UpdateCreate, CreateUpdateDish
from app.database import SessionLocal
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from settings import settings

app = FastAPI(title='Ylab Restaurant')

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_headers=['*'],
    allow_methods=['*'],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_main():
    return {"msg": "Hello Ylab"}


@app.get("/api/v1/menus",
         response_model=list[BaseMenu])
def get_menus(db: Session = Depends(get_db)):
    """Get all menus"""
    menus = db.query(Menu).all()
    return menus if menus else []


@app.get("/api/v1/menus/{menu_id}",
         response_model=BaseMenu)
def get_menu(menu_id: int,
             db: Session = Depends(get_db)
             ) -> BaseMenu:
    """Get one menu  by id"""
    return crud.get_menu(menu_id, db)


@app.post("/api/v1/menus",
          response_model=UpdateCreate)
def create_menu(menu: UpdateCreate,
                db: Session = Depends(get_db)
                ) -> BaseMenu:
    """Create new menu"""
    return crud.create_menu(menu, db)


@app.patch("/api/v1/menus/{id}",
           response_model=UpdateCreate)
def update_menu(menu_id: int,
                menu: UpdateCreate,
                db: Session = Depends(get_db)
                ) -> BaseMenu:
    """Update one menu"""
    return crud.update_menu(menu_id, menu, db)


@app.delete("/api/v1/menus/{id}",
            response_model=BaseDelete)
def delete_menu(id: int,
                db: Session = Depends(get_db)
                ) -> BaseDelete:
    """Delete_menu some menu by id"""
    return crud.delete_menu(id, db)


@app.get("/api/v1/menus/{menu_id}/submenus")
def get_submenus(menu_id: int,
                 db: Session = Depends(get_db)
                 ) -> list[BaseSubmenu]:
    """Get all submenus by menu id"""
    return crud.get_submenus(menu_id, db)


@app.post("/api/v1/menus/{menu_id}/submenus", response_model=BaseSubmenu)
def create_submenu(menu_id: int,
                   sub: UpdateCreate,
                   db: Session = Depends(get_db)
                   ) -> BaseSubmenu:
    """Create new submenu in menu"""
    return crud.create_submenu(menu_id, sub, db)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}",
         response_model=BaseSubmenu, status_code=200)
def get_submenu(menu_id: int,
                submenu_id: int,
                db: Session = Depends(get_db)
                ) -> BaseSubmenu:
    """Get one submenu by two id"""
    return crud.get_submenu(menu_id, submenu_id, db)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=BaseSubmenu)
def update_submenu(menu_id: int,
                   submenu_id: int,
                   sub: UpdateCreate,
                   db: Session = Depends(get_db)
                   ) -> BaseSubmenu:
    """Update one submenu by menu id"""
    return crud.update_submenu(menu_id, submenu_id, sub, db)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: int,
                   submenu_id: int,
                   db: Session = Depends(get_db)
                   ) -> BaseDelete:
    """Delete one submenu by menu id"""
    return crud.delete_submenu(menu_id, submenu_id, db)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
def get_dishes(menu_id: int,
               submenu_id: int,
               db: Session = Depends(get_db)
               ) -> list[BaseDish]:
    """Get all dishes by menu and submenu id"""
    return crud.get_dishes(menu_id, submenu_id, db)


@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=BaseDish)
def create_dish(menu_id: int,
                submenu_id: int,
                dish: CreateUpdateDish,
                db: Session = Depends(get_db)
                ) -> BaseDish:
    """Create new dish"""
    return crud.create_dish(menu_id, submenu_id, dish, db)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
         response_model=BaseDish)
def get_dish(menu_id: int,
             submenu_id: int,
             dish_id: int,
             db: Session = Depends(get_db)
             ) -> BaseDish:
    """Get some dish by id"""
    return crud.get_dish(menu_id, submenu_id, dish_id, db)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
           response_model=BaseDish)
def update_dish(menu_id: int,
                submenu_id: int,
                dish_id: int,
                dish: CreateUpdateDish,
                db: Session = Depends(get_db)
                ) -> BaseDish:
    """Update one dish by id"""
    return crud.update_dish(menu_id, submenu_id, dish_id, dish, db)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
            response_model=BaseDelete)
def delete_dish(menu_id: int,
                submenu_id: int,
                dish_id: int,
                db: Session = Depends(get_db)
                ) -> BaseDelete:
    """Delete some dish by id"""
    return crud.delete_dish(menu_id, submenu_id, dish_id, db)


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)
