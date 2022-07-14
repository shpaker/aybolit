from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

from aybolit.enums import States


@dataclass(frozen=True)
class ProbeResult:
    state: States
    message: Optional[str]
    finished_at: datetime
    timespan: timedelta


@dataclass(frozen=True)
class HealthyResult:
    results: List[ProbeResult]

    @property
    def state(self) -> States:
        state = States.PASS
        for probe in self.results:
            if probe.state is States.FAIL:
                state = States.FAIL
                continue
            if probe.state is States.ERROR:
                return States.ERROR
        return state
