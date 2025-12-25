# pylint: disable=missing-module-docstring, missing-class-docstring

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from workout_api.configs.database import Base

class WorkoutModel(Base):
    __tablename__ = "workout"

    id: int = Column(Integer, primary_key=True)
    athlete_id: int = Column(Integer, ForeignKey("athlete.id"), nullable=False)
    name: str = Column(String(50), nullable=False)
    sport_modality: str = Column(String(50), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    athlete = relationship("AthleteModel", back_populates="workout")
