from pydantic import BaseModel


class ChildSchema(BaseModel):

    imie: str
    dob: str

    class Config:
        from_attributes = True
        populate_by_name = True






