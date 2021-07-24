class NotAdminException(Exception):
    # Admin権限を持ってない場合に飛ぶException
    ...


class NotMemberException(Exception):
    # Member権限を持ってない場合に飛ぶException
    ...


class UnexpectedLeagueStatusException(Exception):
    # League#status の値が期待していない値となっている場合のException
    ...


class UnexpectedArgsException(Exception):
    # GetまたはPostメソッドにて、期待した引数が存在しない場合のException
    ...


class UnexpectedValueException(Exception):
    # GetまたはPostメソッドにて、期待した引数の値が想定外のものとなっている場合のException
    ...
