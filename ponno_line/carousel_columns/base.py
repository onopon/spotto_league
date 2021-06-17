from typing import Optional
from abc import abstractmethod
from linebot.models import CarouselColumn


class Base:
    @abstractmethod
    def create(self, **kwargs) -> Optional[CarouselColumn]:
        pass
