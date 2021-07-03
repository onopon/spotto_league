from typing import Dict, Any
import requests
from tests.base import Base
from instance import settings
from requests.models import Response

URI_FORMAT = 'http://127.0.0.1:80{}'
ses = requests.Session()


class BaseController(Base):
    def login(self, login_name: str, plain_password: str) -> None:
        args = {'login_name': login_name,
                'password': plain_password,
                'common_password': settings.COMMON_PASSWORD}
        self.post("/user/login", args)

    def logout(self) -> None:
        self.get("/user/logout")

    def get(self, url_path: str, args: Dict={}) -> Response:
        url = URI_FORMAT.format(url_path)
        # argsは後回し
        if args:
            pass
        return ses.get(url)

    def post(self, url_path: str, args: Dict={}) -> Response:
        return ses.post(URI_FORMAT.format(url_path), data=args)

    # override
    def tear_down(self):
        super().tear_down()
        self.logout()
