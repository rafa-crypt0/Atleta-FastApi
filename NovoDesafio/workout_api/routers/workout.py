# pylint: disable=missing-module-docstring, missing-function-docstring, import-error

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from workout_api.configs.database import get_session
from workout_api.models.workout import WorkoutModel
from workout_api.models.athlete import AthleteModel
from workout_api.schemas.workout import WorkoutIn, WorkoutOut, WorkoutUpdate

router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.post("/", response_model=WorkoutOut, status_code=status.HTTP_201_CREATED)
async def create_workout(data: WorkoutIn, db: AsyncSession = Depends(get_session)):

    # verificar se o atleta existe
    result = await db.execute(select(AthleteModel).where(AthleteModel.id == data.athlete_id))
    athlete = result.scalar_one_or_none()

    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")

    workout = WorkoutModel(**data.model_dump())
    db.add(workout)
    await db.commit()
    await db.refresh(workout)
    return workout


@router.get("/", response_model=list[WorkoutOut])
async def list_workouts(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(WorkoutModel))
    return result.scalars().all()


@router.get("/{workout_id}", response_model=WorkoutOut)
async def get_workout(workout_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(WorkoutModel).where(WorkoutModel.id == workout_id))
    workout = result.scalar_one_or_none()

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    return workout


@router.patch("/{workout_id}", response_model=WorkoutOut)
async def update_workout(
    workout_id: int,
    updates: WorkoutUpdate,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(select(WorkoutModel).where(WorkoutModel.id == workout_id))
    workout = result.scalar_one_or_none()

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(workout, key, value)

    await db.commit()
    await db.refresh(workout)
    return workout


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(workout_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(WorkoutModel).where(WorkoutModel.id == workout_id))
    workout = result.scalar_one_or_none()

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    await db.delete(workout)
    await db.commit()
