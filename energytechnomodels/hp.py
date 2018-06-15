import numpy as np
from scipy.integrate import odeint
from energytechnomodels.base import Model, tau_model


class HeatPump(Model):
    """Model class of a HP dynamic model based on a ratio of the theoretical COP of Carnot"""

    def __init__(
        self,
        p_max,
        t_snk,
        t_src,
        n_th=0.4,
        tau=60.0,
        io_init=0.0,
        start="1/1/2000",
    ):
        super().__init__(start)
        assert t_snk > t_src

        self.p_max = p_max
        self.t_src = t_src
        self.t_snk = t_snk

        self.n_th = n_th
        self.tau = tau

        self.io = io_init

        self.cop = self.n_th * ((self.t_snk + 273.15) / (self.t_snk - self.t_src))

        self.p_sink = self.io * self.p_max
        self.p_elec = self.p_sink / self.cop
        self.p_srce = self.p_sink - self.p_elec

    def step(self, step, unit="seconds"):
        super().step(step, unit)

        t = np.arange(start=0, stop=step * self.UNIT[unit], step=1.0)

        res_p_sink = odeint(
            tau_model, self.p_sink, t, args=(self.io, self.tau, self.p_max)
        )

        self.cop = self.n_th * ((self.t_snk + 273.15) / (self.t_snk - self.t_src))

        self.p_sink = round(res_p_sink[-1][0])
        self.p_elec = self.p_sink / self.cop
        self.p_srce = self.p_sink - self.p_elec
