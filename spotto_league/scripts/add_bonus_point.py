import os
import argparse
from spotto_league.models.user import User
from spotto_league.models.bonus_point import BonusPoint
from spotto_league.models.role import Role, RoleType
from .base import Base


class AddBonusPoint(Base):
    # override
    def execute_task(self, login_name: str, point: int) -> None:
        try:
            user = User.find_by_login_name(login_name)
            bonus_point = BonusPoint.find_or_initialize_by_user_id(user.id)
            bonus_point.point = point
            bonus_point.save()
        except Exception as e:
            print("エラーが発生しました。 {}".format(e.args))

if __name__ == '__main__':
    '''
    使用例)
    maguに勝つと1500ポイントボーナスでもらえるようにする場合。
    poetry run python -m spotto_league.scripts.add_bonus_point --login_name=magu --point=1500
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--login_name', required=True, type=str)
    parser.add_argument('--point', required=True, type=int)
    args = parser.parse_args()
    AddBonusPoint().execute(login_name=args.login_name, point=args.point)
    print('Done')
