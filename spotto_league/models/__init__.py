from typing import List, Any
from .user import User
from .user_point import UserPoint
from .league import League
from .league_log import LeagueLog
from .league_log_detail import LeagueLogDetail
from .league_member import LeagueMember
from .role import Role
from .place import Place
from .bonus_point import BonusPoint
from .league_point import LeaguePoint

__all__ = [
    "User",
    "UserPoint",
    "League",
    "LeagueLog",
    "LeagueLogDetail",
    "LeagueMember",
    "Role",
    "Place",
    "BonusPoint",
    "LeaguePoint",
]


def all() -> List[Any]:
    return [
        User,
        UserPoint,
        League,
        LeagueLog,
        LeagueLogDetail,
        LeagueMember,
        Role,
        Place,
        BonusPoint,
        LeaguePoint,
    ]
