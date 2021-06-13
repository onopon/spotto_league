from typing import Optional
from abc import ABCMeta, abstractmethod
from linebot.models import CarouselColumn
from instance import settings


class Base:
    @abstractmethod
    def create(self, **kwargs) -> Optional[CarouselColumn]:
        pass
