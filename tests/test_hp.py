import pytest
from energytechnomodels import HeatPump


@pytest.fixture()
def fix_create():
    hp = HeatPump(200, 55.0, 10.0)
    hp.io = 1
    hp.step(2, "minutes")
    return hp


def test_hp_step(fix_create):
    hp = fix_create
    assert round(hp.cop, 2) == 2.92
    assert round(hp.p_sink, 2) == 172.48
