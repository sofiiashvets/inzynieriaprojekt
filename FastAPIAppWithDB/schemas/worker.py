from typing import List

from pydantic import BaseModel, ConfigDict
from sqlalchemy.dialects.postgresql import JSONB


class WorkerSchema(BaseModel):
   
    pesel: str
    imie: str
    nazwisko: str
    age: int
    criminal_record: bool

    children: List
    # salary: List[SalarySchema]
    department_id: int = None

    class Config:
        from_attributes = True
        populate_by_name = True