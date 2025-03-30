import pytest
from app import schemas
from jose import jwt
from app.config import settings

def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json().get('message') == 'Welcome to the FastAPI application!'

def test_create_user(client):
    response = client.post('/users', json={
        'email': 'johndoe@example.com',
        'password': 'secret'
    })

    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == 'johndoe@example.com'
    assert response.status_code == 201

def test_login_user(client, test_user):
    response = client.post('/login', data={
        'username': test_user['email'],
        'password': test_user['password']
    })

    assert response.status_code == 200

    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")

    assert login_res.token_type == 'bearer'
    assert id == test_user['id']

@pytest.mark.parametrize("email, password, status_code", [
    ('wrong_email@example.com','secret', 403),
    ('johndoe@example.com', 'wrong_password', 403),
    ('wrong_email@example.com', 'wrong_password', 403),
    (None, 'secret', 422),
    ('johndoe@example.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    login_data = {}
    if email is not None:
        login_data['username'] = email
    if password is not None:
        login_data['password'] = password

    response = client.post('/login', data=login_data)
    assert response.status_code == status_code