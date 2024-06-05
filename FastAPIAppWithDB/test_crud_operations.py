import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models.worker import Worker
from models.department import Department
from schemas.worker import WorkerSchema
from schemas.department import DepartmentSchema
from crud.crud_workers import CRUDWorkers
from crud.crud_department import CRUDDepartment

# Set up the test database
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/study', echo=False, pool_size=50, max_overflow=100"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Initialize the CRUD classes
crud_workers = CRUDWorkers()
crud_department = CRUDDepartment()

@pytest.fixture(scope="module")
def db():
    """Create a new database session for a test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_worker(db):
    worker_data = WorkerSchema(
        pesel="1234567890",
        imie="John",
        nazwisko="Doe",
        age=30,
        criminal_record=False,
        children=[],
        department_id=None
    )
    created_worker = crud_workers.add_or_update(db, worker_data)
    assert created_worker.pesel == worker_data.pesel
    assert created_worker.imie == worker_data.imie
    assert created_worker.nazwisko == worker_data.nazwisko

def test_get_worker(db):
    worker = crud_workers.get(db, 1234567890)
    assert worker is not None
    assert worker.pesel == "1234567890"

def test_update_worker(db):
    worker_data = WorkerSchema(
        pesel="1234567890",
        imie="Jane",
        nazwisko="Doe",
        age=32,
        criminal_record=False,
        children=[],
        department_id=None
    )
    updated_worker = crud_workers.add_or_update(db, worker_data)
    assert updated_worker.imie == "Jane"
    assert updated_worker.age == 32

def test_delete_worker(db):
    result = crud_workers.delete(db, "1234567890")
    assert result is True
    worker = crud_workers.get(db, 1234567890)
    assert worker is None

def test_create_department(db):
    department_data = DepartmentSchema(
        id=1,
        name="HR",
        street="Main St",
        city="Anytown",
        postcode="12345"
    )
    created_department = crud_department.add_or_update(db, department_data)
    assert created_department.id == department_data.id
    assert created_department.name == department_data.name

def test_get_department(db):
    department = crud_department.get(db, 1)
    assert department is not None
    assert department.name == "HR"

def test_update_department(db):
    department_data = DepartmentSchema(
        id=1,
        name="Human Resources",
        street="Main St",
        city="Anytown",
        postcode="12345"
    )
    updated_department = crud_department.add_or_update(db, department_data)
    assert updated_department.name == "Human Resources"

def test_delete_department(db):
    result = crud_department.delete(db, 1)
    assert result is True
    department = crud_department.get(db, 1)
    assert department is None