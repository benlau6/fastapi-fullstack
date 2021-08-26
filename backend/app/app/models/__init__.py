from .team import Team, TeamRead, TeamCreate, TeamUpdate#, TeamReadWithHeroes
from .hero import Hero, HeroRead, HeroCreate, HeroUpdate#, HeroReadWithTeam

from typing import List, Optional

class TeamReadWithHeroes(TeamRead):
    heroes: List[HeroRead] = []

class HeroReadWithTeam(HeroRead):
    team: Optional[TeamRead] = None
    