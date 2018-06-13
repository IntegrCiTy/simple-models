import pytest
from energytechnomodels import CombinedHeatPower


@pytest.fixture()
def fix_create():
    chp = CombinedHeatPower(200)
    chp.t_ret = 55.0
    chp.step(1, "minutes")
    return chp


def test_chp_step(fix_create):
    chp = fix_create
    assert chp.t_sup == 80.57
