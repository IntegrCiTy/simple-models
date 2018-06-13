import pandas as pd


def tau_model(y, t, io, tau, p_nom):
    """Define ODE for a simplified dynamic model using time constant"""
    dydt = (p_nom * io - y) / tau
    return dydt


class Model:

    UNIT = {"seconds": 1, "minutes": 60, "hours": 3600}

    def __init__(self, start):
        """"""
        self.time = pd.to_datetime(start)

    def step(self, step, unit):
        """"""
        self.time += pd.DateOffset(**{unit: step})
