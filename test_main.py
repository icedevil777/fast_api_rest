from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_one_menu():
    response = client.get('/api/v1/menus/0')
    assert response.json() == {'detail': 'menu not found'}


def test_get_sub(client):
    response = client.get('/api/v1/menus/0/submenus')
    assert response.json() == []