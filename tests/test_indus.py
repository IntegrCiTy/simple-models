import pytest
from energytechnomodels import Bath


@pytest.fixture()
def fix_create():
    b = Bath(2.7, 2.7, t_bath_init=50.0)
    b.p_heat = 50E3
    b.step(2, "hours")
    return b


def test_chp_step(fix_create):
    b = fix_create
    assert round(b.t_bath, 2) == 66.98
