from typing import Optional
from abc import abstractmethod
from linebot.models.template import Template


class Base:
    @abstractmethod
    def create(self, **kwargs) -> Optional[Template]:
        pass
