# pylint: disable=missing-module-docstring, missing-class-docstring

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from workout_api.configs.database import Base

class AthleteModel(Base):
    __tablename__ = "athlete"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(50), nullable=False)
    cpf: str = Column(String(11), unique=True, nullable=False)
    age: int = Column(Integer, nullable=False)

    workout = relationship("WorkoutModel", back_populates="athlete")
