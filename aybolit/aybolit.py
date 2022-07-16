from abc import ABC, abstractmethod
from asyncio import iscoroutinefunction
from datetime import datetime, timedelta
from typing import Any, Callable, List, Optional, Union

from aybolit.results import CheckResult
from aybolit.wrappers import AsyncCheckDefWrapper, CheckDefWrapper


class _AybolitBase(ABC):
    def __init__(
        self,
    ) -> None:
        pass
        self._check_defs: List[
            Union[CheckDefWrapper, AsyncCheckDefWrapper]
        ] = []

    def __call__(
        self,
        title: Optional[str] = None,
        result_ttl: Union[int, timedelta] = 0,
    ) -> Callable:
        def wrapper(
            func: Callable,
        ) -> None:
            self.add(
                check_def=func,
                title=title,
                result_ttl=result_ttl,
            )

        return wrapper

    def add(
        self,
        check_def: Callable[[], Any],
        title: Optional[str] = None,
        result_ttl: Union[int, timedelta] = 0,
    ) -> None:
        title = title if title else check_def.__name__
        wrapper_cls = (
            AsyncCheckDefWrapper
            if iscoroutinefunction(check_def)
            else CheckDefWrapper
        )
        self._check_defs.append(
            wrapper_cls(  # type: ignore
                check_def=check_def,
                title=title,
                result_ttl=result_ttl,
            )
        )

    @abstractmethod
    def check(
        self,
        **kwargs: Any,
    ) -> CheckResult:
        raise NotImplementedError


class Aybolit(_AybolitBase):
    def check(
        self,
        **kwargs: Any,
    ) -> CheckResult:
        checks = []
        started_at = datetime.now()
        for check_def in self._check_defs:
            kwargs = {
                key: value
                for key, value in kwargs.items()
                if key in check_def.kwargs_keys
            }
            result = check_def(**kwargs)
            checks.append(result)
        return CheckResult(
            checks=checks,
            started_at=started_at,
            finished_at=datetime.now(),
        )


class AsyncAybolit(_AybolitBase):
    async def check(
        self,
        **kwargs: Any,
    ) -> CheckResult:
        checks = []
        started_at = datetime.now()
        for check_def in self._check_defs:
            kwargs = {
                key: value
                for key, value in kwargs.items()
                if key in check_def.kwargs_keys
            }
            result = (
                await check_def(**kwargs)
                if check_def.is_async
                else check_def(**kwargs)
            )
            checks.append(result)
        return CheckResult(
            checks=checks,
            started_at=started_at,
            finished_at=datetime.now(),
        )
