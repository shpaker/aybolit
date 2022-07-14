class HealthyBaseError(Exception):
    ...


class ProbeFail(HealthyBaseError):
    ...


class ProbeError(HealthyBaseError):
    ...
