import uvicorn
from starlette import status
from . import crud
from app import models
from app.database import engine
from app.models import Menu, Submenu, Dish
from app.schemas import BaseMenu, CreateMenu, BaseDelete, BaseDish
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
          response_model=CreateMenu)
def create_menu(menu: CreateMenu,
                db: Session = Depends(get_db)
                ) -> BaseMenu:
    """Create new menu"""
    return crud.create_menu(menu, db)


@app.patch("/api/v1/menus/{id}",
           response_model=CreateMenu)
def update_menu(menu_id: int,
                menu: CreateMenu,
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
                 ) -> list[BaseMenu]:
    """Get all submenus by menu id"""
    return crud.get_submenus(menu_id, db)


#
#
@app.post("/api/v1/menus/{menu_id}/submenus", status_code=201)
def create_submenu(menu_id: int,
                   db: Session = Depends(get_db)
                   ):
    """Create new submenu"""
    return crud.create_submenu(menu_id, db)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def get_submenu(menu_id: int,
                submenu_id: int,
                db: Session = Depends(get_db)
                ):
    """Get some submenu by id"""
    return crud.get_submenu(menu_id, submenu_id, db)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", status_code=200)
def update_submenu(menu_id: int,
                   submenu_id: int,
                   db: Session = Depends(get_db)
                   ):
    """Update one submenu by menu id"""
    return crud.update_submenu(menu_id, submenu_id, db)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: int,
                   submenu_id: int,
                   db: Session = Depends(get_db)
                   ):
    """Delete one submenu by menu id"""
    return crud.delete_submenu(menu_id, submenu_id, db)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
def get_dishes(menu_id: int,
               submenu_id: int,
               db: Session = Depends(get_db)
               ):
    """Get all dishes by menu and submenu id"""
    return crud.get_dishes(menu_id, submenu_id, db)


@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
          status_code=201)
def create_dish(menu_id: int,
                submenu_id: int,
                db: Session = Depends(get_db)
                ):
    """Create new dish"""
    return crud.create_dish(menu_id, submenu_id, db)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def get_dish(menu_id: int,
             submenu_id: int,
             dish_id: int,
             db: Session = Depends(get_db)
             ):
    """Get some dish by id"""
    return crud.get_dish(menu_id, submenu_id, dish_id, db)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
           status_code=200)
def update_dish(menu_id: int,
                submenu_id: int,
                dish_id: int,
                dish: BaseDish,
                db: Session = Depends(get_db)
                ):
    """Update one dish by id"""
    return crud.update_dish(menu_id, submenu_id, dish_id, dish, db)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(menu_id: int,
                submenu_id: int,
                dish_id: int,
                db: Session = Depends(get_db)
                ) -> BaseDelete:
    """Delete some dish by id"""
    return crud.delete_dish(menu_id, submenu_id, dish_id, db)



if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)
