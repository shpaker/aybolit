from abc import ABC, abstractmethod
from asyncio import iscoroutinefunction
from datetime import datetime, timedelta
from inspect import signature
from typing import Any, Callable, Optional, Union

from aybolit.enums import CheckDefState
from aybolit.exceptions import ProbeError, ProbeFail
from aybolit.results import CheckDefWrapperResult
from aybolit.utils import state_and_message_from_exc


class CheckDefBaseWrapper(ABC):
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

    @property
    def is_async(self):
        return iscoroutinefunction(self._check_def)

    @abstractmethod
    def __call__(
        self,
        **kwargs: Any,
    ) -> CheckDefWrapperResult:
        raise NotImplementedError

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

    def _get_check_state_from_exc(
        self,
        exc: Union[AssertionError, ProbeFail, ProbeError],
    ) -> CheckDefState:
        if exc.__class__ in (AssertionError, ProbeFail):
            return CheckDefState.FAIL
        return CheckDefState.ERROR


class CheckDefWrapper(CheckDefBaseWrapper):
    def __call__(
        self,
        **kwargs: Any,
    ) -> CheckDefWrapperResult:
        state = CheckDefState.PASS
        started_at = datetime.now()
        if self._result and self._is_ttl_valid(started_at):
            return self._result

        try:
            message = self._check_def(**kwargs)
        except Exception as exc:
            state, message = state_and_message_from_exc(exc)

        self._finished_at = datetime.now()
        self._result = CheckDefWrapperResult(
            title=self._title,
            state=state,
            message=message,
            started_at=started_at,
            finished_at=self._finished_at,
        )
        return self._result


class AsyncCheckDefWrapper(CheckDefBaseWrapper):
    async def __call__(
        self,
        **kwargs: Any,
    ) -> CheckDefWrapperResult:
        state = CheckDefState.PASS
        started_at = datetime.now()
        if self._result and self._is_ttl_valid(started_at):
            return self._result

        try:
            message = await self._check_def(**kwargs)
        except Exception as exc:
            state, message = state_and_message_from_exc(exc)

        self._finished_at = datetime.now()
        self._result = CheckDefWrapperResult(
            title=self._title,
            state=state,
            message=message,
            started_at=started_at,
            finished_at=self._finished_at,
        )
        return self._result
