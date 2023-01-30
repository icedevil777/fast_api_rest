import asyncio
import pytest
from app.main import app
from httpx import AsyncClient


@pytest.fixture(scope="session")
def event_loop():
	return asyncio.get_event_loop()


@pytest.mark.asyncio
async def test_root():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get("/")
	assert response.status_code == 200
	assert response.json() == {"msg": "Hello Ylab"}


@pytest.mark.asyncio
async def test_get_menus():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get("/api/v1/menus")
	assert response.json() == []
	assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_menu_0():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get('/api/v1/menus/0')
	assert response.status_code == 404
	assert response.json() == {'detail': "menu not found"}


@pytest.mark.asyncio
async def test_create_menu():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post(
			'/api/v1/menus',
			json={
				'title': 'My menu 1',
				'description': 'My menu description 1',
			}
		)
	assert response.status_code == 201
	assert response.json() == {
		"id": "1",
		"title": "My menu 1",
		"description": "My menu description 1",
		'dishes_count': 0,
		'submenus_count': 0
	}


@pytest.mark.asyncio
async def test_get_menu_1():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get('/api/v1/menus/1')
	assert response.json() == {
		"id": "1",
		"title": "My menu 1",
		"description": "My menu description 1",
		"submenus_count": 0,
		"dishes_count": 0
	}


@pytest.mark.asyncio
async def test_update_menu():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.patch(
			'/api/v1/menus/1/',
			json={
				'title': 'My updated menu 2',
				'description': 'My updated menu description 2',
			}
		)
	# assert response.status_code == 200
	assert response.json() == {
		"id": "1",
		"title": "My updated menu 2",
		"description": "My updated menu description 2",
		"submenus_count": 0,
		"dishes_count": 0,
	}


@pytest.mark.asyncio
async def test_delete_menu():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.delete('/api/v1/menus/1')
	assert response.json() == {
		"status": True,
		"message": "The menu has been deleted"
	}


@pytest.mark.asyncio
async def test_patch_menu_after_delete():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.patch(
			'/api/v1/menus/1',
			json={
				'title': 'My updated menu 1',
				'description': 'My updated menu description 1'
			}
		)
	assert response.json() == {'detail': 'menu not found'}


@pytest.mark.asyncio
async def test_delete_menu_2():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.delete('/api/v1/menus/30')
	assert response.json() == {"detail": "menu not found"}


@pytest.mark.asyncio
async def test_create_menu_2():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post(
			'/api/v1/menus',
			json={
				'title': 'My menu 2',
				'description': 'My menu description 2'
			}
		)
	assert response.json() == {
		"id": '2',
		"title": "My menu 2",
		"description": "My menu description 2",
		"submenus_count": 0,
		"dishes_count": 0,
	}


@pytest.mark.asyncio
async def test_get_sub():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get('/api/v1/menus/2/submenus')
	assert response.status_code == 200
	assert response.json() == []


@pytest.mark.asyncio
async def test_post_submenu():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post(
			'/api/v1/menus/2/submenus',
			json={
				'title': 'My submenu 1',
				'description': 'My submenu description 1',
			}
		)
	assert response.json() == {
		"id": "1",
		"title": "My submenu 1",
		"description": "My submenu description 1",
		"dishes_count": 0,
	}


@pytest.mark.asyncio
async def test_get_sub_one_not():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get('/api/v1/menus/2/submenus/10')
	assert response.status_code == 404
	assert response.json() == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_patch_submenu():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.patch(
			'/api/v1/menus/2/submenus/1',
			json={
				'title': 'My update submenu 1',
				'description': 'My update submenu description 1'
			}
		)
	assert response.json() == {
		"id": '1',
		"title": "My update submenu 1",
		"description": "My update submenu description 1",
		"dishes_count": 0,
	}


@pytest.mark.asyncio
async def test_del_submenu():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.delete(
			'/api/v1/menus/2/submenus/1'
		)
	assert response.json() == {
		"status": True,
		"message": "The submenu has been deleted"
	}


@pytest.mark.asyncio
async def test_post_submenu_agen():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post(
			'/api/v1/menus/2/submenus',
			json={
				'title': 'My submenu 2',
				'description': 'My submenu description 2'
			}
		)
	assert response.json() == {
		"id": "2",
		"title": "My submenu 2",
		"description": "My submenu description 2",
		"dishes_count": 0
	}


@pytest.mark.asyncio
async def test_get_list_dishes():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get('/api/v1/menus/2/submenus/2/dishes')
	assert response.json() == []


@pytest.mark.asyncio
async def testing_add_dish():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post(
			'/api/v1/menus/2/submenus/2/dishes',
			json={
				"title": "My dish 1",
				"description": "My dish description 1",
				"price": '10.5'
			}
		)
	assert response.json() == {
		"id": "1",
		"title": "My dish 1",
		"description": "My dish description 1",
		"price": "10.5",
	}


@pytest.mark.asyncio
async def test_patch_dish():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.patch(
			'/api/v1/menus/2/submenus/2/dishes/1',
			json={
				"title": "My updated dish 1",
				"description": "My updated dish description 1",
				"price": "14.5"
			}
		)
	assert response.json() == {
		"id": "1",
		"title": "My updated dish 1",
		"description": "My updated dish description 1",
		"price": "14.5"
	}


@pytest.mark.asyncio
async def test_get_one_dish():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get('/api/v1/menus/2/submenus/2/dishes/1')
	assert response.json() == {
		"id": "1",
		"title": "My updated dish 1",
		"description": "My updated dish description 1",
		"price": "14.5"
	}


@pytest.mark.asyncio
async def test_delete_dish_empty():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get('/api/v1/menus/2/submenus/2/dishes/10')
	assert response.status_code == 404
	assert response.json() == {'detail': 'dish not found'}


@pytest.mark.asyncio
async def test_delete_menu_1():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.delete('/api/v1/menus/2')
	assert response.status_code == 200
	assert response.json() == {
		"status": True,
		"message": "The menu has been deleted"
	}
