# coding=utf8

from webargs.flaskparser import parser


@parser.error_handler
def argerror_handler(e):
    raise Error(Error.ARGUMENT_ERROR, e.message)


class Error(Exception):
    """
    User custom error
    """
    " 0 ~ 1000 System Error "
    BOOTSTRAP_ERROR = 0
    ARGUMENT_ERROR = 1
    DATABASE_ERROR = 2

    " 1000 ~ fin User Error "
    USER_NOT_FOUND = 1000
    USER_EXISTED = 1001
    USER_OR_PASS_ERROR = 1002

    TOKEN_INVALID = 1010

    translate = {
        BOOTSTRAP_ERROR: u'系统内部错误',
        ARGUMENT_ERROR: u'参数错误',
        DATABASE_ERROR: u'数据库错误',

        USER_NOT_FOUND: u'用户不存在',
        USER_EXISTED: u'用户已存在',
        USER_OR_PASS_ERROR: u'用户名或密码错误',

        TOKEN_INVALID: u'无效的Token'
    }

    def __init__(self, code=0, message="", *args, **kwargs):
        self.error_code = code
        self.message = message or self.translate.get(self.error_code)

    def __str__(self):
        return self.message.encode('utf8')
