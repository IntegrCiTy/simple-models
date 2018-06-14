import numpy as np
from energytechnomodels.base import Model
from thermo.chemical import Chemical


water = Chemical("water", P=3E5, T=273.15 + 50)


def cc(ntu, cr):
    return (1 - np.exp(-ntu * (1 - cr))) / (1 - cr * np.exp(-ntu * (1 - cr)))


def pp(ntu, cr):
    return (1 - np.exp(-ntu * (1 - cr))) / (1 + cr)


class HeatExchanger(Model):
    """Model class of a heat exchanger using e-NTU method"""

    GEOMETRY = {"counter-current": cc, "parallel": pp}

    def __init__(
        self,
        t_i_src,
        t_i_snk,
        m_dot_src,
        m_dot_snk,
        A,
        U,
        fluid_src=water,
        fluid_snk=water,
        geo="counter-current",
        start="1/1/2000",
    ):
        super().__init__(start)

        self.A = A
        self.U = U
        self.geo = geo

        self.t_i_src = t_i_src
        self.t_i_snk = t_i_snk

        self.m_dot_src = m_dot_src
        self.m_dot_snk = m_dot_snk

        self.fluid_src = fluid_src
        self.fluid_snk = fluid_snk

        self.t_o_src = None
        self.t_o_snk = None

    def step(self, step, unit="seconds"):
        super().step(step, unit)

        c_min = min(
            self.m_dot_src * self.fluid_src.Cp, self.m_dot_snk * self.fluid_snk.Cp
        )
        c_max = max(
            self.m_dot_src * self.fluid_src.Cp, self.m_dot_snk * self.fluid_snk.Cp
        )

        c_r = c_min / c_max

        ntu = self.U * self.A / c_min

        eff = self.GEOMETRY[self.geo](ntu, c_r)

        q = eff * c_min * (self.t_i_src - self.t_i_snk)

        self.t_o_src = round(self.t_i_src - q / (self.m_dot_src * self.fluid_src.Cp), 2)
        self.t_o_snk = round(self.t_i_snk + q / (self.m_dot_snk * self.fluid_snk.Cp), 2)
