import os
import argparse
from spotto_league.models.league_point import LeaguePoint
from .base import Base


class AddLeaguePoint(Base):
    # override
    def execute_task(self) -> None:
        try:
            if (len(LeaguePoint.all())):
                raise Exception("既存データが存在するため、実行できません。")
            league_point_list = [[1, 1, 3000],
                                 [1, 2, 2000],
                                 [1, 3, 1500],
                                 [1, 4, 1200],
                                 [1, 5, 1000],
                                 [1, 6, 900],
                                 [1, 7, 800],
                                 [1, 8, 700],
                                 [1, 9, 600],
                                 [1, 10, 500],
                                 [1, 11, 400],
                                 [1, 12, 300],
                                 [2, 1, 3000 * 1.5],
                                 [2, 2, 2000 * 1.5],
                                 [2, 3, 1500 * 1.5],
                                 [2, 4, 1200 * 1.5],
                                 [2, 5, 1000 * 1.5],
                                 [2, 6, 900 * 1.5],
                                 [2, 7, 800 * 1.5],
                                 [2, 8, 700 * 1.5],
                                 [2, 9, 600 * 1.5],
                                 [2, 10, 500 * 1.5],
                                 [2, 11, 400 * 1.5],
                                 [2, 12, 300 * 1.5],
                                 [3, 1, 3000 * 2],
                                 [3, 2, 2000 * 2],
                                 [3, 3, 1500 * 2],
                                 [3, 4, 1200 * 2],
                                 [3, 5, 1000 * 2],
                                 [3, 6, 900 * 2],
                                 [3, 7, 800 * 2],
                                 [3, 8, 700 * 2],
                                 [3, 9, 600 * 2],
                                 [3, 10, 500 * 2],
                                 [3, 11, 400 * 2],
                                 [3, 12, 300 * 2]]
            for data in league_point_list:
                league_point = LeaguePoint()
                league_point.group_id = data[0]
                league_point.rank = data[1]
                league_point.point = data[2]
                league_point.save()
        except Exception as e:
            print("エラーが発生しました。 {}".format(e.args))

if __name__ == '__main__':
    '''
    使用例)
    ※ 最初の1度だけ使うことを想定しているので、2度目以降はDBのデータを一度truncateしてから使うことをお勧めします。
    poetry run python -m spotto_league.scripts.add_league_point
    '''
    AddLeaguePoint().execute()
    print('Done')
