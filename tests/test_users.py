from app import schemas
from .database import client, session

def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to the FastAPI application!'}

def test_create_user(client):
    response = client.post('/users', json={
        'email': 'johndoe@example.com',
        'password': 'secret'
    })

    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == 'johndoe@example.com'
    assert response.status_code == 201