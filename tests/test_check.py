from pytest import mark, param

from healthy import Aybolit
from healthy.exceptions import ProbeError, ProbeFail
from healthy.probe_wrapper import States

_TEST_MSG = 'foo'


def pass_check():
    pass


def pass_check_params(foo):
    return foo


def pass_check_with_msg():
    return _TEST_MSG


def fail_check():
    raise ProbeFail


def fail_check_with_msg():
    raise ProbeFail(_TEST_MSG)


def assert_check():
    assert 1 == 2


def assert_msg_check():
    assert 1 == 2, _TEST_MSG


def error_check():
    1 // 0


def error_check_with_msg():
    raise ProbeError(_TEST_MSG)


@mark.parametrize(
    ('probe_func', 'state', 'message'),
    (
        param(pass_check, States.PASS, None),
        param(pass_check_with_msg, States.PASS, _TEST_MSG),
        param(pass_check_params, States.PASS, _TEST_MSG),
        param(fail_check, States.FAIL, None),
        param(fail_check_with_msg, States.FAIL, _TEST_MSG),
        param(assert_check, States.FAIL, None),
        param(assert_msg_check, States.FAIL, _TEST_MSG),
        param(
            error_check,
            States.ERROR,
            'ZeroDivisionError: integer division or modulo by zero',
        ),
        param(error_check_with_msg, States.ERROR, _TEST_MSG),
    ),
)
def test_check(
    state,
    probe_func,
    message,
) -> None:
    healthy = Aybolit()
    healthy.add_check(probe_func)
    result = healthy.run(foo=_TEST_MSG)
    common_state = result.state
    assert common_state == state
    probe = result.results[0]
    assert probe.message == message
