import pytest
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture(scope='module')
def client():
    client = TestClient(app=app)
    yield client


def test_get_menus(client):
    response = client.get('/api/v1/menus')
    assert response.json() == []
    assert response.status_code == 200


def test_get_menu(client):
    response = client.get('/api/v1/menus/0')
    assert response.json() == {'detail': "Not Found"}


def test_create_menu(client):
    response = client.post('/api/v1/menus',
                           json={'title': 'My menu 1', 'description': 'My menu description 1'})

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "My menu 1",
        "description": "My menu description 1",
    }


def test_get_menu_1(client):
    response = client.get('/api/v1/menus/1')
    assert response.json() == {
        "id": 1,
        "title": "My menu 1",
        "description": "My menu description 1",
        # "submenus_count": 0,
        # "dishes_count": 0
    }


def test_update_menu(client):
    response = client.patch('/api/v1/menus/1/',
                            json={'title': 'My updated menu 2', 'description': 'My updated menu description 2'})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "My updated menu 2",
        "description": "My updated menu description 2"
        # "submenus_count": 0,
        # "dishes_count": 0
    }


def test_delete_menu(client):
    response = client.delete('/api/v1/menus/1')
    assert response.json() == {
        "status": True,
        "message": "It's deleted"
    }


def test_patch_menu_after_delete(client):
    response = client.patch('/api/v1/menus/1',
                            json={'title': 'My updated menu 1', 'description': 'My updated menu description 1'})
    assert response.json() == {'detail': 'Not Found'}


def test_delete_menu_2(client):
    response = client.delete('/api/v1/menus/30')
    assert response.json() == {"detail": "Not Found"}


def test_create_menu_2(client):
    response = client.post('/api/v1/menus', json={'title': 'My menu 2', 'description': 'My menu description 2'})
    assert response.json() == {
        "id": 2,
        "title": "My menu 2",
        "description": "My menu description 2",
        # "submenus_count": 0,
        # "dishes_count": 0
    }


def test_get_sub(client):
    response = client.get('/api/v1/menus/2/submenus')
    assert response.json() == {'detail': 'Not Found'}


def test_post_submenu(client):
    response = client.post('/api/v1/menus/2/submenus',
                           json={'title': 'My submenu 1', 'description': 'My submenu description 1'})
    assert response.json() == {
        "id": 1,
        "menu_id": 2,
        "title": "My submenu 1",
        "description": "My submenu description 1",
        # "dishes_count": 0
    }


def test_get_sub_one_not(client):
    response = client.get('/api/v1/menus/2/submenus/10')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_patch_submenu(client):
    response = client.patch('/api/v1/menus/2/submenus/1',
                            json={'title': 'My update submenu 1', 'description': 'My update submenu description 1'})
    assert response.json() == {
        "id": 1,
        "menu_id": 2,
        "title": "My update submenu 1",
        "description": "My update submenu description 1",
        # "dishes_count": 0
    }


def test_del_submenu(client):
    response = client.delete('/api/v1/menus/2/submenus/1')
    assert response.json() == {
        "status": True,
        "message": "It's deleted"
    }


def test_post_submenu_agen(client):
    response = client.post('/api/v1/menus/2/submenus', json={'title': 'My submenu 2',
                                                             'description': 'My submenu description 2'})
    assert response.json() == {
        "id": 2,
        "menu_id": 2,
        "title": "My submenu 2",
        "description": "My submenu description 2",
        # "dishes_count": 0
    }


def test_get_list_dishes(client):
    response = client.get('/api/v1/menus/2/submenus/2/dishes')
    assert response.json() == []


def testing_add_dish(client):
    response = client.post(
        '/api/v1/menus/2/submenus/2/dishes',
        json={
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": 10.5
        }
    )

    assert response.json() == {
        "id": 1,
        "menu_id": 2,
        "submenu_id": 2,
        "title": "My dish 1",
        "price": 10.5,
        "description": "My dish description 1"
    }


def test_patch_dish(client):
    response = client.patch(
        '/api/v1/menus/2/submenus/2/dishes/1',
        json={
            "title": "My updated dish 1",
            "description": "My updated dish description 1",
            "price": 14.5
        }
    )
    assert response.json() == {
        "id": 1,
        "menu_id": 2,
        "submenu_id": 2,
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": 14.5
    }


def test_get_one_dish(client):
    response = client.get('/api/v1/menus/2/submenus/2/dishes/1')
    assert response.json() == {
        "id": 1,
        "menu_id": 2,
        "submenu_id": 2,
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": 14.5
    }


def test_delete_dish_empty(client):
    response = client.get('/api/v1/menus/2/submenus/2/dishes/10')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_delete_menu_1(client):
    response = client.delete('/api/v1/menus/2')
    assert response.status_code == 200
    assert response.json() == {
        "status": True,
        "message": "It's deleted"
    }
