from abc import ABCMeta, abstractmethod
from typing import Optional
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    Message,
    MessageEvent
)


class Base:
    __slots__ = ['_event']
    def __init__(self, event: MessageEvent) -> None:
        self._event = event

    @property
    def event(self) -> MessageEvent:
        return self._event

    # Reply用
    # replyの条件を満たしているかどうかを確認するメソッド
    @abstractmethod
    def satisfy_react_condition(self, **kwargs) -> bool:
        pass

    # Reply用
    # reply用のMessageをcreateする
    @abstractmethod
    def create(self, **kwargs) -> Optional[Message]:
        pass

    def getForReply(self, **kwargs) -> Optional[Message]:
        if not self.satisfy_react_condition(**kwargs):
            return None
        return self.create(**kwargs)

