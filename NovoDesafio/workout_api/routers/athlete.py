# pylint: disable=missing-module-docstring, missing-function-docstring, import-error

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from workout_api.configs.database import get_session
from workout_api.models.athlete import AthleteModel
from workout_api.schemas.athlete import AthleteIn, AthleteOut, AthleteUpdate

router = APIRouter(prefix="/athletes", tags=["Athletes"])


@router.post("/", response_model=AthleteOut, status_code=status.HTTP_201_CREATED)
async def create_athlete(data: AthleteIn, db: AsyncSession = Depends(get_session)):
    athlete = AthleteModel(**data.model_dump())
    db.add(athlete)
    await db.commit()
    await db.refresh(athlete)
    return athlete


@router.get("/", response_model=list[AthleteOut])
async def list_athletes(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(AthleteModel))
    return result.scalars().all()


@router.get("/{athlete_id}", response_model=AthleteOut)
async def get_athlete(athlete_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(AthleteModel).where(AthleteModel.id == athlete_id))
    athlete = result.scalar_one_or_none()

    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")

    return athlete


@router.patch("/{athlete_id}", response_model=AthleteOut)
async def update_athlete(
    athlete_id: int,
    updates: AthleteUpdate,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(select(AthleteModel).where(AthleteModel.id == athlete_id))
    athlete = result.scalar_one_or_none()

    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")

    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(athlete, key, value)

    await db.commit()
    await db.refresh(athlete)
    return athlete


@router.delete("/{athlete_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_athlete(athlete_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(AthleteModel).where(AthleteModel.id == athlete_id))
    athlete = result.scalar_one_or_none()

    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")

    await db.delete(athlete)
    await db.commit()
