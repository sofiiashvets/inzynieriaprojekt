from typing import List

from pydantic import BaseModel

from schemas.worker import WorkerSchema


class DepartmentSchema(BaseModel):
    id: int
    name: str
    street: str
    city: str
    postcode: str
    workers_no: int = 0

    class Config:
        from_attributes = True
        populate_by_name = True


class DepartmentSchemaCreate(BaseModel):
    id: int
    name: str
    street: str
    city: str
    postcode: str

    class Config:
        from_attributes = True
        populate_by_name = True


class DepartmentSchemaWL(BaseModel):
    id: int
    name: str
    street: str
    city: str
    postcode: str
    workers: List[WorkerSchema] = []

    class Config:
        from_attributes = True
        populate_by_name = True
