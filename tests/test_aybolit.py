from pytest import mark, param

from aybolit import AsyncAybolit, Aybolit
from aybolit.exceptions import ProbeError, ProbeFail
from aybolit.wrappers import CheckDefState

_TEST_MSG = 'foo'


def pass_check():
    pass


def pass_check_with_msg():
    return _TEST_MSG


def pass_check_params(foo):
    return foo


def fail_check():
    raise ProbeFail


def fail_check_with_msg():
    raise ProbeFail(_TEST_MSG)


def assert_check():
    assert 1 == 2


def assert_msg_check():
    assert 1 == 2, _TEST_MSG


def error_check():
    42 // 0


def error_check_with_msg():
    raise ProbeError(_TEST_MSG)


@mark.parametrize(
    ('probe_func', 'state', 'message'),
    (
        param(pass_check, CheckDefState.PASS, None),
        param(pass_check_with_msg, CheckDefState.PASS, _TEST_MSG),
        param(pass_check_params, CheckDefState.PASS, _TEST_MSG),
        param(pass_check_params, CheckDefState.PASS, _TEST_MSG),
        param(fail_check, CheckDefState.FAIL, None),
        param(fail_check_with_msg, CheckDefState.FAIL, _TEST_MSG),
        param(assert_check, CheckDefState.FAIL, None),
        param(assert_msg_check, CheckDefState.FAIL, _TEST_MSG),
        param(
            error_check,
            CheckDefState.ERROR,
            'ZeroDivisionError: integer division or modulo by zero',
        ),
        param(error_check_with_msg, CheckDefState.ERROR, _TEST_MSG),
    ),
)
def test_sync(
    state,
    probe_func,
    message,
) -> None:
    aybolit = Aybolit()
    aybolit.add(probe_func)
    result = aybolit.check(foo=_TEST_MSG)
    common_state = result.state
    assert common_state == state
    probe = result.checks[0]
    assert probe.message == message


@mark.asyncio
async def test_async():
    async def _async_def():
        return _TEST_MSG

    aybolit = AsyncAybolit()
    aybolit.add(_async_def)
    result = await aybolit.check()
    common_state = result.state
    assert common_state == CheckDefState.PASS
    probe = result.checks[0]
    assert probe.message == _TEST_MSG
