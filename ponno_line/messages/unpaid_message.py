from typing import Optional
from ponno_line.messages.base import Base
from linebot.models import Message, TextSendMessage
from spotto_league.models.user import User as ModelUser
from spotto_league.models.unpaid import Unpaid as ModelUnpaid


class UnpaidMessage(Base):
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
        unpaid_texts = []
        unpaids = ModelUnpaid.all()
        if not unpaids:
            return None

        for unpaid in unpaids:
            user = ModelUser.find(unpaid.user_id)
            unpaid_texts.append("{}さん: {}円".format(user.name, unpaid.amount))

        texts = ["○諸々の費用未払いの方へご連絡です○"]
        texts.append("下記の方は、次回の練習や電子マネー、お振込等でまぐまさんにご返済ください。")
        texts.append("----------")
        texts.extend(unpaid_texts)
        texts.append("----------")
        texts.append("未払金の詳細はご自身のユーザページにてご確認いただけます。")
        texts.append("また、すでにお支払い済みの方で、こちらにお名前がご記載の方がいらっしゃいましたら、まぐまさんにご連絡ください。")
        texts.append("よろしくお願いいたします。")
        return "\n".join(texts)
