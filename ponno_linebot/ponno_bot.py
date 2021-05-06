from enum import Enum
from typing import Optional, List
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import MessageEvent
from ponno_linebot.messages.base import Base as MessageBase
from ponno_linebot.messages.league_template_send_message import LeagueTemplateSendMessage
import settings


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
        message = LeagueTemplateSendMessage.getForPush(league_id = league_id)
        LineBotApi(settings.LINE_BOT_CHANNEL_ACCESS_TOKEN).push_message(channel, message)
