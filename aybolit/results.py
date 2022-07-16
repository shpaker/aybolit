from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

from aybolit.enums import CheckDefState


@dataclass(frozen=True)
class CheckDefWrapperResult:
    title: str
    state: CheckDefState
    message: Optional[str]
    finished_at: datetime
    timespan: timedelta


@dataclass(frozen=True)
class CheckResult:
    results: List[CheckDefWrapperResult]

    @property
    def state(self) -> CheckDefState:
        state = CheckDefState.PASS
        for result in self.results:
            if result.state is CheckDefState.FAIL:
                state = CheckDefState.FAIL
                continue
            if result.state is CheckDefState.ERROR:
                return CheckDefState.ERROR
        return state
