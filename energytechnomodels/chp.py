import numpy as np
from scipy.integrate import odeint
from thermo.chemical import Chemical
from energytechnomodels.base import Model, tau_model


class CombinedHeatPower(Model):
    """Model class of a combined heat and power plant dynamic model."""

    def __init__(
        self,
        p_nom_kw,
        load_init=1.0,
        fluid=Chemical("water", P=2E5, T=273.15 + 60),
        start="1/1/2000",
    ):
        super().__init__(start)

        self.p_nom_kw = p_nom_kw
        self.fluid = fluid

        self.tau_up_s = 20 * 60
        self.tau_do_s = 10 * 60

        self.load = load_init
        self.load_min = 0.65

        self.eff_el = 0.37
        self.eff_th = 0.52

        self.m_dot = 3.5 / 3600  # m3/s
        self.t_ret = 50

        self.p_el_kw = self.p_nom_kw * self.load * self.eff_el
        self.p_th_kw = self.p_nom_kw * self.load * self.eff_th
        self.p_fu_kw = self.p_nom_kw * self.load
        self.t_sup = round(self.t_ret + self.p_th_kw / self.m_dot / self.fluid.Cp, 2)

    def step(self, step, unit="seconds"):
        super().step(step, unit)

        t = np.arange(start=0, stop=step * self.UNIT[unit], step=1.0)

        run = self.load >= self.load_min
        tau = {True: self.tau_up_s, False: self.tau_do_s}[run]
        load = {True: self.load, False: 0.0}[run]

        res_p_fu_kw = odeint(
            tau_model, self.p_fu_kw, t, args=(load, tau, self.p_nom_kw)
        )
        self.p_fu_kw = round(res_p_fu_kw[-1][0], 3)

        self.p_el_kw = self.p_fu_kw * self.eff_el
        self.p_th_kw = self.p_fu_kw * self.eff_th
        self.t_sup = round(self.t_ret + self.p_th_kw / self.m_dot / self.fluid.Cp, 2)
