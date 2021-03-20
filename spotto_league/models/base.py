from typing import Optional, Any
from spotto_league.database import SpottoDB

db = SpottoDB()


class Base():
    __slots__ = ['_session']
    @property
    def session(self) -> db.session:
        session = SpottoDB().session.object_session(self)
        if session:
            return session
        return SpottoDB().session

    @classmethod
    def find(cls, target_id: int) -> Any:
        return SpottoDB().session.query(cls).filter(cls.id==target_id).one()

    @classmethod
    def find_by_id(cls, target_id: int) -> Optional[Any]:
        return SpottoDB().session.query(cls).filter(cls.id==target_id).one_or_none()

    def save(self) -> None:
        self.session.add(self)
        self.session.commit()

    def delete(self) -> None:
        if not self.id:
            return
        self.session.delete(self)
        self.session.commit()
