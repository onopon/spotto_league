import os
import argparse
from spotto_league.models.user import User
from spotto_league.models.role import Role, RoleType
from .base import Base


class AddRole(Base):
    # override
    def execute_task(self, login_name: str, role_type: int) -> None:
        try:
            user = User.find_by_login_name(login_name)
            role = Role.find_or_initialize_by_user_id(user.id)
            role.role_type = RoleType(role_type).value
            role.save()
        except Exception as e:
            print("エラーが発生しました。 {}".format(e.args))

if __name__ == '__main__':
    '''
    使用例)
    onoponにrole_type=1を付与する場合。
    poetry run python -m spotto_league.scripts.add_role --login_name=onopon --role_type=1
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--login_name', required=True, type=str)
    parser.add_argument('--role_type', required=True, type=int)
    args = parser.parse_args()
    AddRole().execute(login_name=args.login_name, role_type=args.role_type)
    print('Done')
