from abc import ABCMeta, abstractmethod
from spotto_league.app import create_app


class Base(metaclass=ABCMeta):
    @abstractmethod
    def execute_task(self, **kwargs) -> None:
        pass

    def execute(self, **kwargs) -> bool:
        app = create_app()
        with app.app_context():
            return self.execute_task(**kwargs)
