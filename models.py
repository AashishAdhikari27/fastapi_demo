# from pydantic import BaseModel


# class Product(BaseModel):
#     id: int
#     name: str
#     description: str
#     price: float
#     quantity: int


 

## noe converting the above models to sqlmodel

from sqlmodel import SQLModel, Field
from typing import Optional


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # id is optional for auto generation by the database
    name: str
    description: str
    price: float
    quantity: int
