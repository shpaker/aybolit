from datetime import datetime, timedelta
from typing import Any, Callable, List, Optional, Union

from aybolit.results import CheckResult
from aybolit.wrappers import CheckDefWrapper


class Aybolit:
    def __init__(
        self,
    ) -> None:
        pass
        self._check_defs: List[CheckDefWrapper] = []

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
        self._check_defs.append(
            CheckDefWrapper(  # type: ignore
                check_def=check_def,
                title=title,
                result_ttl=result_ttl,
            )
        )

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
            result = await check_def(**kwargs)
            checks.append(result)
        return CheckResult(
            checks=checks,
            started_at=started_at,
            finished_at=datetime.now(),
        )
