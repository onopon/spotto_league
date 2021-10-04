from linebot import LineBotApi
from instance import settings
from unittest.mock import MagicMock, patch
from linebot.exceptions import LineBotApiError
from linebot.models.error import Error


class PonnoLineDecorator:
    settings.LINE_BOT_ENABLE = True

    def line_pushed(self, func):
        def wrapper(*args, **kwargs):
            with patch.object(LineBotApi, 'push_message') as mock_push_message:
                res = func(*args, **kwargs)
                assert mock_push_message.called
            return res
        return wrapper

    def notify_posted(self, func):
        def wrapper(*args, **kwargs):
            api_error = LineBotApiError(429, {}, error=Error(message="You have reached your monthly limit."))
            with patch.object(LineBotApi, 'push_message', MagicMock(side_effect=api_error)):
                with patch('requests.post') as mock_post:
                    res = func(*args, **kwargs)
                    assert mock_post.called
            return res
        return wrapper

    def line_not_pushed(self, func):
        def wrapper(*args, **kwargs):
            with patch.object(LineBotApi, 'push_message') as mock_push_message:
                res = func(*args, **kwargs)
                assert not mock_push_message.called
            return res
        return wrapper


