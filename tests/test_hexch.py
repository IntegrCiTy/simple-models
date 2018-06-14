from energytechnomodels import HeatExchanger


def test_hexh_step_cc():
    he = HeatExchanger(80.0, 20.0, 0.05, 0.02, A=0.5, U=1E3, geo="counter-current")
    he.step(1)
    assert he.t_o_src == 56.4
    assert he.t_o_snk == 79.0


def test_hexh_step_pp():
    he = HeatExchanger(80.0, 20.0, 0.05, 0.02, A=0.5, U=1E3, geo="parallel")
    he.step(1)
    assert he.t_o_src == 63.33
    assert he.t_o_snk == 61.67
