from enum import Enum, auto, unique


@unique
class CheckDefState(str, Enum):
    PASS = auto()
    FAIL = auto()
    ERROR = auto()
