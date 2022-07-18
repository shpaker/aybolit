from asyncio import iscoroutinefunction
from datetime import datetime, timedelta
from inspect import signature
from typing import Any, Callable, Optional, Union

from aybolit.enums import CheckDefState
from aybolit.exceptions import ProbeError, ProbeFail
from aybolit.results import CheckDefWrapperResult
from aybolit.utils import get_error_message_from_assert


class CheckDefWrapper:
    def __init__(
        self,
        check_def: Callable[[], Any],
        title: str,
        result_ttl: Union[int, timedelta],
    ) -> None:
        self._title = title
        self._check_def = check_def
        self.kwargs_keys = signature(check_def).parameters
        self._result_ttl = (
            result_ttl
            if not isinstance(result_ttl, int)
            else timedelta(result_ttl)
        )
        self._result: Optional[CheckDefWrapperResult] = None

    def _is_ttl_valid(
        self,
        timestamp: datetime,
    ) -> bool:
        if not self._result or self._result_ttl == 0:
            return False
        elapsed = timestamp - self._result.finished_at
        if elapsed <= self._result_ttl:
            return True
        return False

    async def _call_check_def(
        self,
        **kwargs,
    ) -> str:
        if iscoroutinefunction(self._check_def):
            return await self._check_def(**kwargs)
        return self._check_def(**kwargs)

    async def __call__(
        self,
        **kwargs: Any,
    ) -> CheckDefWrapperResult:
        state = CheckDefState.PASS
        started_at = datetime.now()
        if self._result and self._is_ttl_valid(started_at):
            return self._result

        try:
            message = await self._call_check_def(**kwargs)
        except AssertionError as exc:
            state = CheckDefState.FAIL
            message = get_error_message_from_assert(exc)
        except ProbeFail as exc:
            state = CheckDefState.FAIL
            message = str(exc)
        except ProbeError as exc:
            state = CheckDefState.ERROR
            message = str(exc)
        except Exception as exc:
            state = CheckDefState.ERROR
            message = f'{exc.__class__.__name__}: {exc}'

        self._finished_at = datetime.now()
        self._result = CheckDefWrapperResult(
            title=self._title,
            state=state,
            message=message if message else None,
            started_at=started_at,
            finished_at=self._finished_at,
        )
        return self._result
