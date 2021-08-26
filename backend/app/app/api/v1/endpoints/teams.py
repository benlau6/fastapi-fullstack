from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app import models
from app.api import deps


router = APIRouter()


@router.post("/teams/", response_model=models.TeamRead)
def create_team(*, session: Session = Depends(deps.get_session), team: models.TeamCreate):
    db_team = models.Team.from_orm(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.get("/teams/", response_model=List[models.TeamRead])
def read_teams(
    *,
    session: Session = Depends(deps.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    teams = session.exec(select(models.Team).offset(offset).limit(limit)).all()
    return teams


@router.get("/teams/{team_id}", response_model=models.TeamReadWithHeroes)
def read_team(*, team_id: int, session: Session = Depends(deps.get_session)):
    team = session.get(models.Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.patch("/teams/{team_id}", response_model=models.TeamRead)
def update_team(
    *,
    session: Session = Depends(deps.get_session),
    team_id: int,
    team: models.TeamUpdate,
):
    db_team = session.get(models.Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.delete("/teams/{team_id}")
def delete_team(*, session: Session = Depends(deps.get_session), team_id: int):
    team = session.get(models.Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"ok": True}