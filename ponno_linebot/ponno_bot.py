import argparse
import json
from enum import Enum
from typing import Optional, List
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import MessageEvent, TextSendMessage
from ponno_linebot.messages.base import Base as MessageBase
from ponno_linebot.messages.league_template_send_message import LeagueTemplateSendMessage
import settings
from spotto_league.app import create_app


class MessageList:
    @classmethod
    def get_by_priority(cls) -> List[MessageBase]:
        return []

class PonnoBot:
    __slots__ = ['_api']
    def __init__(self) -> None:
        self._api = LineBotApi(settings.LINE_BOT_CHANNEL_ACCESS_TOKEN)

    def reply(event: MessageEvent) -> None:
        if not settings.LINE_BOT_ENABLE:
            return

        for message_cls in MessageList.get_by_priority():
            msg = message_cls.get(event)
            if msg:
                self._api.reply_message(event.reply_token, message)
                return

    @classmethod
    def push_about_finished_league(cls, league_id: int, channel: str = None) -> None:
        if not settings.LINE_BOT_ENABLE:
            return

        channel = channel or settings.LINE_BOT_GROUP_ID_HASH[settings.LINE_BOT_ENV]
        message = LeagueTemplateSendMessage.get_for_push_about_finished_league(league_id = league_id)
        LineBotApi(settings.LINE_BOT_CHANNEL_ACCESS_TOKEN).push_message(channel, message)

    @classmethod
    def push_about_cancel_league(cls, league_id: int, channel: str = None) -> None:
        if not settings.LINE_BOT_ENABLE:
            return

        channel = channel or settings.LINE_BOT_GROUP_ID_HASH[settings.LINE_BOT_ENV]
        message = LeagueTemplateSendMessage.get_for_push_about_cacnel_league(league_id = league_id)
        LineBotApi(settings.LINE_BOT_CHANNEL_ACCESS_TOKEN).push_message(channel, message)

    @classmethod
    def push_about_join_end_at_deadline(cls, channel: str = None) -> None:
        if not settings.LINE_BOT_ENABLE:
            return

        channel = channel or settings.LINE_BOT_GROUP_ID_HASH[settings.LINE_BOT_ENV]
        message = LeagueTemplateSendMessage.get_for_push_about_join_end_at_deadline()
        if not message:
            return
        texts = ["締め切りの近い練習会があるみたいだよ！",
                 "参加表明がまだの方はお早めにね！"]
        LineBotApi(settings.LINE_BOT_CHANNEL_ACCESS_TOKEN).push_message(channel, TextSendMessage(text='\n'.join(texts)))
        LineBotApi(settings.LINE_BOT_CHANNEL_ACCESS_TOKEN).push_message(channel, message)

    # league_ids の中で、まだ申し込み中のLeagueを投稿する。
    @classmethod
    def push_about_recruiting_league_information(cls, league_ids: List[int], channel: str = None) -> None:
        if not settings.LINE_BOT_ENABLE:
            return

        channel = channel or settings.LINE_BOT_GROUP_ID_HASH[settings.LINE_BOT_ENV]
        message = LeagueTemplateSendMessage.get_for_push_about_recruiting_leagues(league_ids = league_ids)
        if not message:
            return
        texts = ["募集中の練習会が追加されたみたいだよ！",
                 "ご都合の合う方はどしどし参加表明ボタンを押してね！"]
        LineBotApi(settings.LINE_BOT_CHANNEL_ACCESS_TOKEN).push_message(channel, TextSendMessage(text='\n'.join(texts)))
        LineBotApi(settings.LINE_BOT_CHANNEL_ACCESS_TOKEN).push_message(channel, message)

    @classmethod
    def push_text(cls, text: str, channel: str = None) -> None:
        if not settings.LINE_BOT_ENABLE:
            return

        channel = channel or settings.LINE_BOT_GROUP_ID_HASH[settings.LINE_BOT_ENV]
        LineBotApi(settings.LINE_BOT_CHANNEL_ACCESS_TOKEN).push_message(channel, TextSendMessage(text=text))

if __name__ == '__main__':
    '''
    ex)
    poetry run python -m ponno_linebot.ponno_bot --method_name push_about_finished_league --kwargs '{"league_id": 3}'
    poetry run python -m ponno_linebot.ponno_bot --method_name push_about_join_end_at_deadline
    poetry run python -m ponno_linebot.ponno_bot --method_name push_about_recruiting_league_information --kwargs '{"league_ids": [14, 15]}'
    poetry run python -m ponno_linebot.ponno_bot --method_name push_text --kwargs '{"text": "hoge"}'
    '''
    # ponno_linebotはspotto_leagueと切り分けたからか、appの設定を書かないと機能しない
    app = create_app()
    app.app_context().push()
    parser = argparse.ArgumentParser()
    parser.add_argument('--method_name', required=True, type=str)
    parser.add_argument('--kwargs', type=str, default='{}')
    args = parser.parse_args()
    kwargs = json.loads(args.kwargs)
    getattr(PonnoBot, args.method_name)(**kwargs)
