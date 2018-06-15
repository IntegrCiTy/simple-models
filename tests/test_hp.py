import pytest
from energytechnomodels import HeatPump


@pytest.fixture()
def fix_create():
    hp = HeatPump(50E3, 55.0, 10.0, 0.05, 0.04)
    hp.io = 1
    hp.step(1, "minutes")
    hp.step(1, "minutes")
    hp.step(1, "minutes")
    return hp


def test_hp_step(fix_create):
    hp = fix_create
    assert round(hp.cop, 2) == 2.92
    assert round(hp.p_sink, 2) == 47383
