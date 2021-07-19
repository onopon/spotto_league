from typing import Dict
from tests.base import Base, app
from instance import settings
from requests.models import Response

URI_FORMAT = 'http://127.0.0.1{}'
client = app.test_client()


class BaseController(Base):
    def login(self, login_name: str, plain_password: str) -> None:
        args = {'login_name': login_name,
                'password': plain_password,
                'common_password': settings.COMMON_PASSWORD}
        self.post("/user/login", data=args)

    def logout(self) -> None:
        self.get("/user/logout")

    def get(self, url_path: str, data: Dict={}) -> Response:
        url = URI_FORMAT.format(url_path)
        # argsは後回し
        if data:
            pass
        return client.get(url)

    def post(self, url_path: str, data: Dict={}) -> Response:
        return client.post(URI_FORMAT.format(url_path), data=data)

    # override
    def tear_down(self):
        self.logout()
        client.delete()
        super().tear_down()
