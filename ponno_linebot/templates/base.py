from abc import ABCMeta, abstractmethod
from linebot.models.template import Template
import settings


class Base:
    @abstractmethod
    def create(self, **kwargs) -> Template:
        pass
