from .team import Team, TeamRead, TeamCreate, TeamUpdate  # , TeamReadWithHeroes
from .hero import Hero, HeroRead, HeroCreate, HeroUpdate  # , HeroReadWithTeam
from .user import User
from .student import Student
from .teacher import Teacher
from .course import Course
from .class_model import ClassModel

from typing import List, Optional


class TeamReadWithHeroes(TeamRead):
    heroes: List[HeroRead] = []


class HeroReadWithTeam(HeroRead):
    team: Optional[TeamRead] = None
