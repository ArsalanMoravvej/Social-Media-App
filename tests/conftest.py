
from fastapi.testclient import TestClient
from app.main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from app.database import get_db, Base

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
def test_user(client):
    user_data = {
        'email': 'johndoe@example.com',
        'password': 'secret'
    }
    response = client.post('/users', json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user