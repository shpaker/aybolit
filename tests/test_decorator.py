from aybolit import Aybolit
from aybolit.wrappers import CheckDefState


def test_ok():
    aybolit = Aybolit()
    check_title = 'test-test-test'

    @aybolit(title=check_title)
    def _async_def():
        pass

    result = aybolit.check()
    common_state = result.state
    assert common_state == CheckDefState.PASS
    assert len(result.checks) == 1, result.checks
    assert result.checks[0].title == check_title, result.checks
