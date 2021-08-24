from typing import Optional
from ponno_line.messages.base import Base
from linebot.models import Message, TextSendMessage
from spotto_league.models.user import User as ModelUser
from datetime import date


class BirthdayMessage(Base):
    # override
    def satisfy_react_condition(self, **kwargs) -> bool:
        return False

    # override
    def create(self, **kwargs) -> Optional[Message]:
        return None

    @classmethod
    def get_message(cls) -> Optional[Message]:
        text = cls.get_text()
        if not text:
            return None
        return TextSendMessage(text=text)

    @classmethod
    def get_text(cls) -> Optional[str]:
        today = date.today()
        users = ModelUser.all_on_birthday(today.month, today.day)
        if not users:
            return None
        birthday_user_names = ["{}さん".format(u.name) for u in users]
        texts = ["今日は、"]
        texts.extend(birthday_user_names)
        texts.append("のお誕生日です！")
        texts.append("おめでとうございます！！👏✨✨")
        return "\n".join(texts)
