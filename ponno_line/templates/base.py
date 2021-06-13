from typing import Optional
from abc import ABCMeta, abstractmethod
from linebot.models.template import Template
from instance import settings


class Base:
    @abstractmethod
    def create(self, **kwargs) -> Optional[Template]:
        pass
