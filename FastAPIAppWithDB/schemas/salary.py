from pydantic import BaseModel


class SalarySchema(BaseModel):
    month: int
    amount: int

    class Config:
        from_attributes = True
        populate_by_name = True
