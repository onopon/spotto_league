import argparse
from .base import Base
from decimal import Decimal, ROUND_HALF_UP
from spotto_league.entities.point_rank import PointRank, POINT_HASH_KEY_BASE
from spotto_league.models.user_point import UserPoint


class TakeOverPoint(Base):
    # override
    def execute_task(self, **kwargs) -> None:
        try:
            from_year = int(kwargs["from_year"])
            percent = int(kwargs["percent"])
            from_point_rank_list = PointRank.make_point_rank_list_in_season(from_year)
            for point_rank in from_point_rank_list:
                if not (point_rank.user.is_admin() or point_rank.user.is_member()):
                    continue
                point = int(Decimal(point_rank.current_point * percent / 100).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
                up = UserPoint()
                up.user_id = point_rank.user.id
                up.set_point(point, POINT_HASH_KEY_BASE, "Take Over from {}".format(from_year))
                up.save()
        except Exception as e:
            print("エラーが発生しました。 {}".format(e.args))


if __name__ == "__main__":
    """
    使用例)
    2021年のポイントを今年に8%引き継ぐ場合
    poetry run python -m spotto_league.scripts.take_over_point --from_year=2021 --percent=8
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--from_year", required=True, type=int)
    parser.add_argument("--percent", required=True, type=int)
    args = parser.parse_args()
    TakeOverPoint().execute(
        from_year=args.from_year,
        percent=args.percent
    )
    print("Done")
