import json


class Status:

    def __init__(self, error_code: int, message: str = None):
        self.error_code = error_code
        self.message = message

    def get_code(self):
        """
        get code via Enum name

        :return: error code
        """
        return self.error_code

    def get_msg(self):
        """
        get message via Enum name

        :return: error message
        """
        return self.message


class Errors:
    SUCCESS = Status(0, 'SUCCESS')
    FAIL = Status(-400000, 'FAIL')
    NETWORK_ERROR = Status(-400001, 'network error')
    UNKNOWN_ERROR = Status(-400002, 'unknown error')
    PARAM_IS_NULL = Status(-400003, 'parameters are null')
    PARAM_ILLEGAL = Status(-400004, 'parameters are illegal')
    REPEATED_COMMIT = Status(-400005, 'repeat commit')
    JSON_PARSE_FAIL = Status(-400006, 'json parse error')
    SQL_ERROR = Status(-400007, 'database drop down')
    NOT_FOUND = Status(-400008, 'no such record')
    REQUEST_METHOD_ILLEGAL = Status(-400009, 'request method is illegal')
    REQUEST_ACTION_ILLEGAL = Status(-400010, 'request action is illegal')


if __name__ == '__main__':
    code = Errors.PARAM_ILLEGAL.get_code()
    print("code:", code)
    msg = Errors.PARAM_ILLEGAL.get_msg()
    print("msg:", msg)

