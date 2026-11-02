import sys
from pathlib import Path

# Add backend directory to sys.path so 'app' is importable
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.config import settings
from app.services.career_service import init_career_roles_db
from app.main import app

# Dedicated SQLite test database file
TEST_DB_FILE = Path(__file__).resolve().parent / "test_careerai.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_FILE.as_posix()}"

test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create all tables in test database and seed career roles."""
    if TEST_DB_FILE.exists():
        TEST_DB_FILE.unlink(missing_ok=True)
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    init_career_roles_db(db)
    db.close()
    yield
    # Cleanup after test suite
    if TEST_DB_FILE.exists():
        try:
            TEST_DB_FILE.unlink(missing_ok=True)
        except Exception:
            pass

@pytest.fixture
def db_session():
    """Provide a transactional database session fixture."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def client(db_session):
    """FastAPI TestClient with overridden get_db dependency."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()
