from enum import Enum, unique


@unique
class CheckDefState(str, Enum):
    PASS = 'pass'
    FAIL = 'fail'
    ERROR = 'error'
