from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app import models
from app.api import deps


router = APIRouter()


@router.post("/heroes/", response_model=models.HeroRead)
def create_hero(*, session: Session = Depends(deps.get_session), hero: models.HeroCreate):
    db_hero = models.Hero.from_orm(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.get("/heroes/", response_model=List[models.HeroRead])
def read_heroes(
    *,
    session: Session = Depends(deps.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    heroes = session.exec(select(models.Hero).offset(offset).limit(limit)).all()
    return heroes


@router.get("/heroes/{hero_id}", response_model=models.HeroReadWithTeam)
def read_hero(*, session: Session = Depends(deps.get_session), hero_id: int):
    hero = session.get(models.Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.patch("/heroes/{hero_id}", response_model=models.HeroRead)
def update_hero(
    *, session: Session = Depends(deps.get_session), hero_id: int, hero: models.HeroUpdate
):
    db_hero = session.get(models.Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.delete("/heroes/{hero_id}")
def delete_hero(*, session: Session = Depends(deps.get_session), hero_id: int):

    hero = session.get(models.Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}