from spotto_league.entities.rank import (
    Rank,
    SORT_PROPERTY_WIN,
    SORT_PROPERTY_GAME_OF_DIFFERENCE,
    SORT_PROPERTY_POINT_OF_DIFFERENCE,
    SORT_PROPERTY_LEAGUE_MEMBER_ID
)
from spotto_league.models.league_member import LeagueMember
from spotto_league.models.league_log import LeagueLog
from spotto_league.models.league_log_detail import LeagueLogDetail
from spotto_league.modules.league_settlement_calculator import LeagueSettlementCalculator
from tests.base import Base
from tests.modules.data_creator import DataCreator
import freezegun


class TestRank(Base):
    def test_some_properties(self):
        place = DataCreator().create('place')
        league = DataCreator().create('default_league', overrided_dict={'place_id': place.id})
        users = DataCreator().create('six_member_users')
        for u in users:
            league_member = LeagueMember.find_or_initialize_by_league_id_and_user_id(league.id, u.id)
            league_member.enabled = True
            league_member.save()
        user = users[2]
        league_member = LeagueMember.find_or_initialize_by_league_id_and_user_id(league.id, user.id)

        league_log_2 = LeagueLog.find_or_initialize(league.id, users[1].id, users[2].id)
        league_log_2.save()

        # users[2]を基準として見ているので、
        # users[0] vs users[2] は 2-0でusers[0]の勝ちとなる
        log_details_hash = {0: 'league_log_details_2_0',
                            1: 'league_log_details_1_2',
                            3: 'league_log_details_0_2',
                            4: 'league_log_details_2_1',
                            5: None}
        for (index, yml_title) in log_details_hash.items():
            league_log = LeagueLog.find_or_initialize(league.id, user.id, users[index].id)
            league_log.save()
            if yml_title:
                DataCreator().create(yml_title, overrided_dict={'league_log_id': league_log.id})

        details = LeagueLogDetail.find_all_by_league_log_ids([l.id for l in league.logs])

        # coverage 対応
        rank = Rank(league_member, [], [])
        assert rank.win_point == 0.0

        rank = Rank(league_member, league.logs, details)
        assert rank.league_member == league_member
        assert rank.league_member_id == league_member.id
        assert rank.user_id == user.id
        assert rank.win == 2
        assert rank.lose == 3
        assert rank.logs == league.logs
        assert rank.details == details
        assert rank.user == user
        assert rank.win_point == 0.4
        assert rank.game_of_difference == -2
        assert rank.point_of_difference == -22

        # set_rank
        rank.set_rank(2)
        assert rank.rank == 2

        # set_reason
        rank.set_reason('reason')
        assert rank.reason == 'reason'
        rank.set_reason_for_priority('win')
        assert rank.reason == '単独'
        rank.set_reason_for_priority('game_of_difference')
        assert rank.reason == 'ゲーム数による得失点差: {}'.format(rank.game_of_difference)
        rank.set_reason_for_priority('point_of_difference')
        assert rank.reason == '獲得ポイント数による得失点差: {}'.format(rank.point_of_difference)
        rank.set_reason_for_priority('league_member_id')
        assert rank.reason == '参加表明時刻の差: {}'.format(league_member.created_at)

        # won
        assert not rank.won(users[0].id)
        assert rank.won(users[1].id)
        assert not rank.won(users[3].id)
        assert rank.won(users[4].id)
        assert not rank.won(users[5].id)

        # to_hash
        rank_hash = rank.to_hash()
        assert rank_hash['rank'] == rank.rank
        assert rank_hash['user_name'] == user.name
        assert rank_hash['login_name'] == user.login_name
        assert rank_hash['win'] == rank.win
        assert rank_hash['lose'] == rank.lose
        assert rank_hash['reason'] == rank.reason
        assert not rank_hash['is_withdrawaler']

    def test_to_hash_for_withdrawaler(self):
        user = DataCreator().create('withdrawaler_user')
        league_member = LeagueMember.find_or_initialize_by_league_id_and_user_id(1, user.id)
        rank = Rank(league_member, [], [])
        rank._rank = 1
        rank._reason = ""
        rank_hash = rank.to_hash()
        assert rank_hash['is_withdrawaler']

    def test_make_rank_list(self):
        place = DataCreator().create('place')
        league = DataCreator().create('default_league', overrided_dict={'place_id': place.id})
        league.finish()
        league.save()

        users = DataCreator().create('six_member_users')
        for u in users:
            league_member = LeagueMember.find_or_initialize_by_league_id_and_user_id(league.id, u.id)
            league_member.enabled = True
            league_member.save()
        user = users[2]
        league_member = LeagueMember.find_or_initialize_by_league_id_and_user_id(league.id, user.id)

        league_log_2 = LeagueLog.find_or_initialize(league.id, users[1].id, users[2].id)
        league_log_2.save()

        # users[2]を基準として見ているので、
        # users[0] vs users[2] は 2-0でusers[0]の勝ちとなる
        log_details_hash = {0: 'league_log_details_2_0',
                            1: 'league_log_details_1_2',
                            3: 'league_log_details_0_2',
                            4: 'league_log_details_2_1',
                            5: None}
        for (index, yml_title) in log_details_hash.items():
            league_log = LeagueLog.find_or_initialize(league.id, user.id, users[index].id)
            league_log.save()
            if yml_title:
                DataCreator().create(yml_title, overrided_dict={'league_log_id': league_log.id})
        rank_list = Rank.make_rank_list(league)
        assert len(rank_list) > 1
        assert len(rank_list) == len(league.members)
        sorted_user_ids = ["eda", "uchida", "amon", "independent", "yukinori", "ding"]
        for i, rank in enumerate(rank_list):
            assert rank.rank == i + 1
            assert rank.user.login_name == sorted_user_ids[i]

    def test_sort_rank_list_sort_properties(self):
        users = DataCreator().create('two_member_users')
        place = DataCreator().create('place')
        league = DataCreator().create('default_league', overrided_dict={'place_id': place.id})
        for i, u in enumerate(users):
            frozen_time = '2021-06-30 00:00:{}'.format(i)
            with freezegun.freeze_time(frozen_time):
                league_member = LeagueMember.find_or_initialize_by_league_id_and_user_id(league.id, u.id)
                league_member.enabled = True
                league_member.save()
        league_log = LeagueLog.find_or_initialize(league.id, users[0].id, users[1].id)
        league_log.save()
        DataCreator().create("league_log_details_2_0", overrided_dict={'league_log_id': league_log.id})

        rank_list = [Rank(league.members[0], [league_log], league_log.details),
                     Rank(league.members[1], [league_log], league_log.details)]

        sorted_rank_list = Rank.sort_rank_list(rank_list, SORT_PROPERTY_WIN)
        assert len(sorted_rank_list) == len(rank_list)
        assert sorted_rank_list[0].league_member_id == rank_list[0].league_member_id
        assert sorted_rank_list[0].reason == "単独"
        assert sorted_rank_list[1].league_member_id == rank_list[1].league_member_id
        assert sorted_rank_list[1].reason == "単独"

        sorted_rank_list = Rank.sort_rank_list(rank_list, SORT_PROPERTY_GAME_OF_DIFFERENCE)
        assert len(sorted_rank_list) == len(rank_list)
        assert sorted_rank_list[0].league_member_id == rank_list[0].league_member_id
        assert sorted_rank_list[0].reason == "ゲーム数による得失点差: 2"
        assert sorted_rank_list[1].league_member_id == rank_list[1].league_member_id
        assert sorted_rank_list[1].reason == "ゲーム数による得失点差: -2"

        sorted_rank_list = Rank.sort_rank_list(rank_list, SORT_PROPERTY_POINT_OF_DIFFERENCE)
        assert len(sorted_rank_list) == len(rank_list)
        assert sorted_rank_list[0].league_member_id == rank_list[0].league_member_id
        assert sorted_rank_list[0].reason == "獲得ポイント数による得失点差: 19"
        assert sorted_rank_list[1].league_member_id == rank_list[1].league_member_id
        assert sorted_rank_list[1].reason == "獲得ポイント数による得失点差: -19"

        sorted_rank_list = Rank.sort_rank_list(rank_list, SORT_PROPERTY_LEAGUE_MEMBER_ID)
        assert len(sorted_rank_list) == len(rank_list)
        assert sorted_rank_list[0].league_member_id == rank_list[0].league_member_id
        assert sorted_rank_list[0].reason == "参加表明時刻の差: 2021-06-30 00:00:00"
        assert sorted_rank_list[1].league_member_id == rank_list[1].league_member_id
        assert sorted_rank_list[1].reason == "参加表明時刻の差: 2021-06-30 00:00:01"

    def test_sort_rank_list_direct_confrontation(self):
        place = DataCreator().create('place')
        league = DataCreator().create('default_league', overrided_dict={'place_id': place.id})
        users = DataCreator().create('six_member_users')
        for u in users:
            league_member = LeagueMember.find_or_initialize_by_league_id_and_user_id(league.id, u.id)
            league_member.enabled = True
            league_member.save()

        league_log = LeagueLog.find_or_initialize(league.id, users[0].id, users[2].id)
        league_log.save()
        DataCreator().create('league_log_details_1_2', overrided_dict={'league_log_id': league_log.id})

        league_log = LeagueLog.find_or_initialize(league.id, users[0].id, users[3].id)
        league_log.save()
        DataCreator().create('league_log_details_2_0', overrided_dict={'league_log_id': league_log.id})

        league_log = LeagueLog.find_or_initialize(league.id, users[0].id, users[4].id)
        league_log.save()
        DataCreator().create('league_log_details_2_0', overrided_dict={'league_log_id': league_log.id})

        league_log = LeagueLog.find_or_initialize(league.id, users[0].id, users[5].id)
        league_log.save()
        DataCreator().create('league_log_details_2_0', overrided_dict={'league_log_id': league_log.id})

        league_log = LeagueLog.find_or_initialize(league.id, users[1].id, users[2].id)
        league_log.save()
        DataCreator().create('league_log_details_2_0', overrided_dict={'league_log_id': league_log.id})

        league_log = LeagueLog.find_or_initialize(league.id, users[1].id, users[3].id)
        league_log.save()
        DataCreator().create('league_log_details_2_1', overrided_dict={'league_log_id': league_log.id})

        league_log = LeagueLog.find_or_initialize(league.id, users[1].id, users[4].id)
        league_log.save()
        DataCreator().create('league_log_details_2_0', overrided_dict={'league_log_id': league_log.id})

        league_log = LeagueLog.find_or_initialize(league.id, users[1].id, users[5].id)
        league_log.save()
        DataCreator().create('league_log_details_2_0', overrided_dict={'league_log_id': league_log.id})

        league_log = LeagueLog.find_or_initialize(league.id, users[2].id, users[4].id)
        league_log.save()
        DataCreator().create('league_log_details_2_0', overrided_dict={'league_log_id': league_log.id})

        league_log = LeagueLog.find_or_initialize(league.id, users[2].id, users[5].id)
        league_log.save()
        DataCreator().create('league_log_details_2_0', overrided_dict={'league_log_id': league_log.id})

        league_log = LeagueLog.find_or_initialize(league.id, users[3].id, users[4].id)
        league_log.save()
        DataCreator().create('league_log_details_2_0', overrided_dict={'league_log_id': league_log.id})

        league_log = LeagueLog.find_or_initialize(league.id, users[3].id, users[5].id)
        league_log.save()
        DataCreator().create('league_log_details_2_0', overrided_dict={'league_log_id': league_log.id})

        # user[0] と user[1] の直接対決
        league_log = LeagueLog.find_or_initialize(league.id, users[0].id, users[1].id)
        league_log.save()
        DataCreator().create('league_log_details_2_1', overrided_dict={'league_log_id': league_log.id})

        # user[2] と user[3] の直接対決
        league_log = LeagueLog.find_or_initialize(league.id, users[2].id, users[3].id)
        league_log.save()
        DataCreator().create('league_log_details_0_2', overrided_dict={'league_log_id': league_log.id})

        settlement_hash = LeagueSettlementCalculator.get_settlement_hash(league.members, league.logs)
        rank_list = []
        for member in league.members:
            settlement = settlement_hash[member.user_id]
            rank = Rank(member, settlement["logs"], settlement["details"])
            rank_list.append(rank)

        sorted_rank_list = Rank.sort_rank_list(rank_list, SORT_PROPERTY_WIN)
        assert len(sorted_rank_list) == len(rank_list)
        reason = "うっちー と お☆DING☆DING の直接対決"
        assert sorted_rank_list[0].user_id == users[0].id
        assert sorted_rank_list[0].reason == reason
        assert sorted_rank_list[1].user_id == users[1].id
        assert sorted_rank_list[1].reason == reason

        reason = "千歳亜門 と ディグの支配者 の直接対決"
        assert sorted_rank_list[2].user_id == users[3].id
        assert sorted_rank_list[2].reason == reason
        assert sorted_rank_list[3].user_id == users[2].id
        assert sorted_rank_list[3].reason == reason
