from abc import abstractmethod
from linebot.models import Action


class Base:
    @abstractmethod
    def create(self, **kwargs) -> Action:
        pass
