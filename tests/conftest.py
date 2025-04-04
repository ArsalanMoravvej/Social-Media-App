
from typing import List
from fastapi.testclient import TestClient
from app import models
from app.main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token

db_driver = "postgresql"
db_host = settings.DATABASE_HOSTNAME
db_port = settings.DATABASE_PORT
db_username = settings.DATABASE_USERNAME
db_password = settings.DATABASE_PASSWORD
db_name = "fastapi_test"
 
SQLALCHEMY_DATABASE_URL = f"{db_driver}://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_users(client):
    users_data = [
        {
            'email': 'johndoe@example.com',
            'password': 'secret'
        },
        {
            'email': 'janedoe@example.com',
            'password': 'password'
        }
    ]

    test_users = []
    for user_data in users_data:
        response = client.post('/users', json=user_data)
        assert response.status_code == 201
        new_user = response.json()
        new_user['password'] = user_data['password']
        test_users.append(new_user)

    return test_users

@pytest.fixture
def test_user(test_users):
    return test_users[0]

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers['Authorization'] = f"Bearer {token}"
    return client

@pytest.fixture
def test_posts(test_users, session) -> List[models.Post]:
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_users[0]['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_users[0]['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_users[0]['id']
    },
    {
        "title": "4th title",
        "content": "4th content",
        "owner_id": test_users[1]['id']
    }
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)

    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts