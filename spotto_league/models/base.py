from typing import Optional, Any, List
from spotto_league.database import db


class Base():
    __slots__ = ['_session']
    # 後ほど削除予定
    @property
    def session(self) -> db.session:
        session = db.session.object_session(self)
        if session:
            return session
        return db.session

    @classmethod
    def find(cls, target_id: int) -> Any:
        return db.session.query(cls).filter(cls.id==target_id).one()

    @classmethod
    def find_by_id(cls, target_id: int) -> Optional[Any]:
        return db.session.query(cls).filter(cls.id==target_id).one_or_none()

    @classmethod
    def find_all_by_ids(cls, target_ids: List[int]) -> List[Any]:
        return db.session.query(cls).filter(cls.id.in_(target_ids)).all()

    def save(self) -> None:
        session = db.session.object_session(self) or db.session
        session.add(self)
        session.commit()

    def delete(self) -> None:
        if not self.id:
            return
        session = db.session.object_session(self) or db.session
        session.delete(self)
        session.commit()
