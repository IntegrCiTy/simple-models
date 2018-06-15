import numpy as np
from scipy.integrate import odeint
from thermo.chemical import Chemical
from energytechnomodels.base import Model, tau_model


class HeatPump(Model):
    """Model class of a HP dynamic model based on a ratio of the theoretical COP of Carnot"""

    def __init__(
        self,
        p_max,  # [W]
        t_snk,
        t_src,
        m_dot_snk,
        m_dot_src,
        n_th=0.4,
        tau=60.0,
        io_init=0.0,
        fluid_src="water",
        fluid_snk="water",
        start="1/1/2000",
    ):
        super().__init__(start)
        assert t_snk > t_src

        self.fluid_src = Chemical(fluid_src, T=273.15 + t_src, P=3E5)
        self.fluid_snk = Chemical(fluid_snk, T=273.15 + t_snk, P=3E5)

        self.p_max = p_max
        self.t_src = t_src
        self.t_snk = t_snk

        self.t_i_snk = t_snk - 10.0

        self.m_dot_snk = m_dot_snk
        self.m_dot_src = m_dot_src

        self.n_th = n_th
        self.tau = tau

        self.io = io_init

        self.cop = self.n_th * ((self.t_snk + 273.15) / (self.t_snk - self.t_src))

        self.p_sink = self.io * self.p_max
        self.p_elec = self.p_sink / self.cop
        self.p_srce = self.p_sink - self.p_elec

        self.t_o_snk = self.t_i_snk + self.p_sink / self.m_dot_snk / self.fluid_snk.Cp
        self.t_o_src = self.t_src - self.p_srce / self.m_dot_src / self.fluid_src.Cp

    def step(self, step, unit="seconds"):
        super().step(step, unit)

        self.fluid_src.T = (self.t_src + self.t_o_src) / 2 + 273.15
        self.fluid_snk.T = (self.t_i_snk + self.t_o_snk) / 2 + 273.15

        t = np.arange(start=0, stop=step * self.UNIT[unit], step=1.0)

        res_p_sink = odeint(
            tau_model, self.p_sink, t, args=(self.io, self.tau, self.p_max)
        )

        self.cop = self.n_th * ((self.t_snk + 273.15) / (self.t_snk - self.t_src))

        self.p_sink = round(res_p_sink[-1][0])
        self.p_elec = self.p_sink / self.cop
        self.p_srce = self.p_sink - self.p_elec

        self.t_o_snk = self.t_i_snk + self.p_sink / self.m_dot_snk / self.fluid_snk.Cp
        self.t_o_src = self.t_src - self.p_srce / self.m_dot_src / self.fluid_src.Cp
