import uvicorn
import database as db
from fastapi import FastAPI, Body
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from settings import settings

app = FastAPI(title='Ylab Restaurant')


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


session = db.SessionLocal()


@app.get("/api/v1/menus")
def get_menus() -> list:
    """Get all menus"""
    return session.query(db.Menu).all()


@app.post("/api/v1/menus", status_code=201)
def create_menu(data=Body()) -> dict:
    """Create new menu"""
    new_menu = db.Menu(title=data["title"], description=data["description"])
    session.add(new_menu)
    session.commit()
    return {
        "id": str(new_menu.id),
        "title": new_menu.title,
        "description": new_menu.description
    }


@app.get("/api/v1/menus/{menu_id}")
def get_menu_by_id(menu_id: int):
    """Get some menu by id"""
    target_menu = session.get(db.Menu, menu_id)
    if target_menu is not None:
        submenus = session.query(db.Submenu.id)
        submenus = submenus.filter(db.Submenu.menu_id == menu_id).all()
        dishes_count = 0
        for sub in submenus:
            q = session.query(db.Dish)
            q = q.filter(db.Dish.submenu_id == sub.id).count()
            dishes_count += q
        return {
            "id": str(target_menu.id),
            "title": target_menu.title,
            "description": target_menu.description,
            "submenus_count": len(submenus),
            "dishes_count": dishes_count
        }
    else:
        return JSONResponse(content={"detail": "menu not found"},
                            status_code=404)


@app.patch("/api/v1/menus/{id}", status_code=200)
def update_menu(id: int, data=Body()) -> dict:
    """Update some menu by id"""
    target_menu = session.get(db.Menu, id)
    target_menu.title = data['title']
    target_menu.description = data['description']
    session.commit()
    return {
        "id": str(target_menu.id),
        "title": target_menu.title,
        "description": target_menu.description
    }


@app.delete("/api/v1/menus/{id}")
def delete_menu(id: int) -> dict:
    """Delete_menu some menu by id"""
    target_menu = session.get(db.Menu, id)
    if target_menu is not None:
        session.delete(target_menu)
        session.commit()
    return {
        "status": "true",
        "message": "The menu has been deleted"
    }


@app.get("/api/v1/menus/{menu_id}/submenus")
def get_submenus(menu_id: int) -> list:
    """Get all submenus some menu by id"""
    submenus = session.query(db.Submenu)
    submenus = submenus.filter(db.Submenu.menu_id == menu_id).all()
    return submenus


@app.post("/api/v1/menus/{menu_id}/submenus", status_code=201)
def create_submenu(menu_id: int, data=Body()) -> dict:
    """Create new submenu"""
    new_submenu = db.Submenu(title=data["title"],
                             description=data["description"],
                             menu_id=menu_id)
    session.add(new_submenu)
    session.commit()
    return {
        "id": str(new_submenu.id),
        "title": new_submenu.title,
        "description": new_submenu.description
    }


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def get_submenu_by_id(menu_id: int, submenu_id: int):
    """Get some submenu by id"""
    target_submenu = session.query(db.Submenu)
    target_submenu = target_submenu.filter(db.Submenu.menu_id == menu_id)
    target_submenu = target_submenu.filter(db.Submenu.id == submenu_id).first()
    if target_submenu is not None:
        dishes_count = session.query(db.Dish)
        dishes_count = dishes_count.filter(db.Dish.submenu_id == submenu_id)
        dishes_count = dishes_count.count()
        return {
            "id": str(target_submenu.id),
            "title": target_submenu.title,
            "description": target_submenu.description,
            "dishes_count": dishes_count
        }
    else:
        return JSONResponse(content={"detail": "submenu not found"},
                            status_code=404)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", status_code=200)
def update_submenu(menu_id, submenu_id, data=Body()) -> dict:
    """Update some submenu by id"""
    target_submenu = session.query(db.Submenu)
    target_submenu = target_submenu.filter(db.Submenu.menu_id == menu_id)
    target_submenu = target_submenu.filter(db.Submenu.id == submenu_id).first()
    target_submenu.title = data['title']
    target_submenu.description = data['description']
    session.commit()
    return {"id": str(target_submenu.id),
            "title": target_submenu.title,
            "description": target_submenu.description
            }


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: int, submenu_id: int) -> dict:
    """Delete some submenu by id"""
    target_submenu = session.query(db.Submenu)
    target_submenu = target_submenu.filter(db.Submenu.menu_id == menu_id)
    target_submenu = target_submenu.filter(db.Submenu.id == submenu_id).first()
    if target_submenu is not None:
        session.delete(target_submenu)
        session.commit()
    return {
        "status": "true",
        "message": "The submenu has been deleted"
    }


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
def get_dishes(submenu_id: int) -> list:
    """Get all dishes in submenu"""
    dishes = session.query(db.Dish).filter(db.Dish.submenu_id == submenu_id).all()
    return dishes


@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
          status_code=201)
def create_dish(submenu_id: int, data=Body()) -> dict:
    """Create new dish in submenu"""
    new_dish = db.Dish(title=data["title"],
                       description=data["description"],
                       price=float(data["price"]),
                       submenu_id=submenu_id)
    session.add(new_dish)
    session.commit()
    return {
        "id": str(new_dish.id),
        "title": new_dish.title,
        "description": new_dish.description,
        "price": '{:.2f}'.format(new_dish.price)
    }


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def get_dish_by_id(submenu_id: int, dish_id: int):
    """Get some dish by id"""
    target_dish = session.query(db.Dish)
    target_dish = target_dish.filter(db.Dish.submenu_id == submenu_id)
    target_dish = target_dish.filter(db.Dish.id == dish_id).first()
    if target_dish is not None:
        return {
            "id": str(target_dish.id),
            "title": target_dish.title,
            "description": target_dish.description,
            "price": '{:.2f}'.format(target_dish.price)
        }
    else:
        return JSONResponse(content={"detail": "dish not found"},
                            status_code=404)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
           status_code=200)
def update_dish(submenu_id: int, dish_id: int, data=Body()) -> dict:
    """Update some dish by id"""
    target_dish = session.query(db.Dish)
    target_dish = target_dish.filter(db.Dish.submenu_id == submenu_id)
    target_dish = target_dish.filter(db.Dish.id == dish_id).first()
    target_dish.title = data['title']
    target_dish.description = data['description']
    target_dish.price = float(data["price"])
    session.commit()
    return {
        "id": str(target_dish.id),
        "title": target_dish.title,
        "description": target_dish.description,
        "price": data["price"]
    }


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(submenu_id: int, dish_id: int) -> dict:
    """Delete some dish by id"""
    target_dish = session.query(db.Dish)
    target_dish = target_dish.filter(db.Dish.submenu_id == submenu_id)
    target_dish = target_dish.filter(db.Dish.id == dish_id).first()
    if target_dish is not None:
        session.delete(target_dish)
        session.commit()
    return {
        "status": "true",
        "message": "The dish has been deleted"
    }


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)
