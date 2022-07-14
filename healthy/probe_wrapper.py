from datetime import datetime, timedelta
from inspect import signature
from typing import Callable, Union, Optional, Any

from healthy.enums import States
from healthy.exceptions import ProbeFail, ProbeError
from healthy.results import ProbeResult
from healthy.utils import get_error_message_from_assert


class ProbeWrapper:

    def __init__(
        self,
        func: Callable[[], Any],
        title: str,
        result_ttl: Union[int, timedelta],
    ) -> None:
        self._title = title
        self._check = func
        self.kwargs_keys = signature(func).parameters
        self._result_ttl = result_ttl if isinstance(result_ttl, int) else timedelta(result_ttl)
        self._result: Optional[ProbeResult] = None

    def _check_ttl_valid(
        self,
        timestamp: datetime,
    ) -> bool:
        if not self._result or self._result_ttl == 0:
            return False
        elapsed = timestamp - self._result.finished_at
        if elapsed <= self._result_ttl:
            return True
        return False

    def __call__(self, **kwargs):
        state = States.PASS
        started_at = datetime.now()
        if self._check_ttl_valid(started_at):
            return self._result

        try:
            message = self._check(**kwargs)
        except AssertionError as exc:
            state = state.FAIL
            message = get_error_message_from_assert(exc)
        except ProbeFail as exc:
            state = state.FAIL
            message = str(exc)
        except ProbeError as exc:
            state = state.ERROR
            message = str(exc)
        except Exception as exc:
            state = state.ERROR
            message = f'{exc.__class__.__name__}: {exc}'

        self._finished_at = datetime.now()
        self._result = ProbeResult(
            state=state,
            message=message if message else None,
            finished_at=self._finished_at,
            timespan=self._finished_at-started_at,
        )
        return self._result
