from linebot.models import Action, URIAction
from ponno_line.actions.base import Base

DEFAULT_LABEL = "詳細を見る"


class DetailURIAction(Base):
    # override
    def create(self, **kwargs) -> Action:
        uri = kwargs["uri"]
        label = kwargs.get("label", DEFAULT_LABEL)
        return URIAction(label=label, uri=uri)
