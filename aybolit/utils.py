from typing import Optional, Tuple

from aybolit.enums import CheckDefState
from aybolit.exceptions import ProbeError, ProbeFail


def get_error_message_from_assert(exc: Exception) -> Optional[str]:
    message = exc.args[0]
    if '\n' not in message:
        return None
    return message.split('\n')[0]


def state_and_message_from_exc(
    exc: Exception,
) -> Tuple['CheckDefState', Optional[str]]:
    if exc.__class__ is AssertionError:
        return CheckDefState.FAIL, get_error_message_from_assert(exc)
    if exc.__class__ is ProbeFail:
        return CheckDefState.FAIL, str(exc) or None
    if exc.__class__ is ProbeError:
        return CheckDefState.ERROR, str(exc) or None
    return CheckDefState.ERROR, f'{exc.__class__.__name__}: {exc}'
