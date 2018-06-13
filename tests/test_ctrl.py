import pytest
from energytechnomodels import Hysteresis


@pytest.fixture()
def fix_create():
    h = Hysteresis()
    h.x = -0.1
    h.step(1, "minutes")
    return h


def test_chp_step(fix_create):
    h = fix_create
    assert h.y == 1
    h.x = 1.1
    h.step(1)
    assert h.y == 0
