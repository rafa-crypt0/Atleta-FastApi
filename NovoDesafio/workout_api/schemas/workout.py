# pylint: disable=missing-module-docstring, missing-class-docstring

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class WorkoutIn(BaseModel):
    athlete_id: int
    name: str = Field(max_length=50)
    sport_modality: str = Field(max_length=50)

class WorkoutOut(BaseModel):
    id: int
    athlete_id: int
    name: str
    sport_modality: str
    created_at: datetime

    class Config:
        from_attributes = True

class WorkoutUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    sport_modality: Optional[str] = Field(None, max_length=50)
