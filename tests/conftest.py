import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# 1. Importujemy obiekt settings i aplikację
from zadania.config import settings
from zadania.main import app
from zadania.database import Base, get_db
from zadania.security import get_password_hash
from zadania.models import User

@pytest.fixture(scope="session", autouse=True)
def setup_test_settings():
    settings.secret_key = "TESTING1234"
    settings.algorithm = "HS256"
    settings.access_token_expire_minutes = 60

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Tworzenie tabel przed każdym testem
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Usuwanie tabel po teście (czysta karta)
        Base.metadata.drop_all(bind=engine)

# 4. Klient testowy
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

# 5. Użytkownicy pomocniczy (Fixtures)
@pytest.fixture
def admin_user(db_session):
    password = "admin_password"
    hashed = get_password_hash(password)
    user = User(
        email="admin@test.pl",
        hashed_password=hashed,
        roles="ROLE_ADMIN,ROLE_USER"
    )
    db_session.add(user)
    db_session.commit()
    return {"email": "admin@test.pl", "password": password}

@pytest.fixture
def regular_user(db_session):
    password = "user_password"
    hashed = get_password_hash(password)
    user = User(
        email="user@test.pl",
        hashed_password=hashed,
        roles="ROLE_USER"
    )
    db_session.add(user)
    db_session.commit()
    return {"email": "user@test.pl", "password": password}