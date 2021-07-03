class NotAdminException(Exception):
    # Admin権限を持ってない場合に飛ぶException
    ...


class NotMemberException(Exception):
    # Member権限を持ってない場合に飛ぶException
    ...
