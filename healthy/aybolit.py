from datetime import timedelta
from typing import List, Callable, Union, Optional, Any

from healthy.probe_wrapper import ProbeWrapper
from healthy.results import HealthyResult


class Aybolit:

    def __init__(
        self,
    ) -> None:
        pass
        self.checks: List[ProbeWrapper] = []

    def __call__(
        self,
        title: Optional[str] = None,
        result_ttl: Union[int, timedelta] = 0,
    ) -> Callable:

        def wrapper(func):
            self.add_check(
                func=func,
                title=title,
                result_ttl=result_ttl,
            )

        return wrapper

    def add_check(
        self,
        func: Callable[[], Any],
        title: Optional[str] = None,
        result_ttl: Union[int, timedelta] = 0,
    ) -> None:
        title = title if title else func.__name__
        self.checks.append(
            ProbeWrapper(
                func=func,
                title=title,
                result_ttl=result_ttl,
            )
        )

    def run(
        self,
        **kwargs,
    ) -> HealthyResult:
        results = []
        for check in self.checks:
            kwargs = {key: value for key, value in kwargs.items() if key in check.kwargs_keys}
            result = check(**kwargs)
            results.append(result)
        return HealthyResult(results=results)
