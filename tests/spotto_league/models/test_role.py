from tests.base import Base
from spotto_league.models.role import RoleType


class TestRoleType(Base):
    def test_all(self):
        role_types = RoleType.all()
        ids = [role_type["id"] for role_type in role_types]
        assert RoleType.ADMIN.value in ids
        assert RoleType.MEMBER.value in ids
        assert not RoleType.GUEST.value in ids
        assert not RoleType.VISITOR.value in ids
