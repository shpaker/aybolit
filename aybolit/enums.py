from enum import Enum


class States(str, Enum):
    PASS = 'pass'
    FAIL = 'fail'
    ERROR = 'error'
