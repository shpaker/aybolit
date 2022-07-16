from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from aybolit.enums import CheckDefState


@dataclass(frozen=True)
class _ResultBase(ABC):
    started_at: datetime
    finished_at: datetime


@dataclass(frozen=True)
class CheckDefWrapperResult(_ResultBase):
    title: str
    state: CheckDefState
    message: Optional[str]


@dataclass(frozen=True)
class CheckResult(_ResultBase):
    checks: List[CheckDefWrapperResult]

    @property
    def state(self) -> CheckDefState:
        state = CheckDefState.PASS
        for result in self.checks:
            if result.state is CheckDefState.FAIL:
                state = CheckDefState.FAIL
                continue
            if result.state is CheckDefState.ERROR:
                return CheckDefState.ERROR
        return state
