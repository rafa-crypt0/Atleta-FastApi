# pylint: disable=missing-module-docstring, missing-class-docstring

from pydantic import BaseModel, Field
from typing import Optional

class AthleteIn(BaseModel):
    name: str = Field(max_length=50)
    cpf: str = Field(max_length=11)
    age: int = Field(gt=0)

class AthleteOut(BaseModel):
    id: int
    name: str
    cpf: str
    age: int

    class Config:
        from_attributes = True

class AthleteUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    age: Optional[int] = Field(None, gt=0)
