import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database import Base, get_db
from app.main import app
from app import crud, auth

# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_bmi_app.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    # Create the test database and tables
    Base.metadata.create_all(bind=engine)

    # Create a new session for each test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

    # Drop all tables after the test is complete
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    # Override the get_db dependency
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # Initialize BMI categories
    crud.initialize_bmi_categories(db_session)

    # Create a test client
    with TestClient(app) as test_client:
        yield test_client

    # Clean up the dependency override
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(client, db_session):
    # Create a test user
    user_data = {"username": "testuser", "password": "password123"}
    user = crud.create_user(db_session, schemas.UserCreate(**user_data))
    return user


@pytest.fixture
def token(client, test_user):
    # Login and get a token
    response = client.post("/token", data={
        "username": "testuser",
        "password": "password123"
    })
    return response.json()["access_token"]


@pytest.fixture
def authorized_client(client, token):
    # Create an authorized client with the token
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client
