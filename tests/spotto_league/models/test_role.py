from tests.base import Base
from spotto_league.models.role import Role, RoleType


class TestRoleType(Base):
    def test_all(self):
        role_types = RoleType.all()
        ids = [role_type["id"] for role_type in role_types]
        assert RoleType.ADMIN.value in ids
        assert RoleType.MEMBER.value in ids
        assert RoleType.WITHDRAWALER.value in ids
        assert RoleType.GUEST.value not in ids
        assert RoleType.VISITOR.value not in ids

    def test_is_in_team(self):
        role = Role()
        role.role_type = RoleType.ADMIN.value
        assert role.is_in_team()

        role.role_type = RoleType.MEMBER.value
        assert role.is_in_team()

        role.role_type = RoleType.GUEST.value
        assert not role.is_in_team()

        role.role_type = RoleType.VISITOR.value
        assert not role.is_in_team()

        role.role_type = RoleType.WITHDRAWALER.value
        assert not role.is_in_team()
