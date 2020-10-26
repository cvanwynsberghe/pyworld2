# -*- coding: utf-8 -*-

# Copyright (c) 2020 Charles Vanwynsberghe

# Pyworld2 is a Python implementation of the World2 model designed by Jay W.
# Forrester, and thouroughly described in the book World Dynamics (1971). It
# is written for educational and research purposes.
# Pyworld2 is forked from the Software Rworld2 held by Arnaud Mignan (2020).

# Licensed under the MIT license:

#     http://www.opensource.org/licenses/mit-license.php

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import json
import os

import numpy as np
from scipy.interpolate import interp1d

from .utils import Clipper, plot_world_state


class World2:
    """
    World2 class contains helpers to configure and run a simulation. Defaults
    parameters leads to a standard run.

    Examples
    --------
    >>> w2 = World2()              # possibly modify time limits and step
    >>> w2.set_state_variables()   # possibly modify the model constants
    >>> w2.set_initial_state()     # possibly modify the condition constants
    >>> w2.set_table_functions()   # possibly do your own tables in a json file
    >>> w2.set_switch_functions()  # possibly choose switches in a json file
    >>> w2.run()                   # run the simulation

    Attributes
    ----------
    year_min : int
        starting year of the simulation.
    year_max : int
        end year of the simulation.
    dt : float
        time step of the numerical integration [year].
    time : numpy.ndarray
        time from year_min to year_max sampled every dt on n points [year].
    n : int
        number of time steps of the numerical integration.
    p : numpy.ndarray
        P - Population [people]. It is a state variable.
    br : numpy.ndarray
        BR - Birth Rate [people/year].
    dr : numpy.ndarray
        DR - Death Rate [people/year].
    cr : numpy.ndarray
        CR - Crowding Ratio [].
    la : float
        LA - Land Area [square kilometers].
    pdn : float
        PDN - Population Density Normal [people/square kilometer].
    nr : numpy.ndarray
        NR - Natural Resources [natural resource units]. It is a state variable.
    nrur : numpy.ndarray
        NRUR - Natural-Resource-Usage Rate [natural resource units/year].
    nrfr : numpy.ndarray
        NRFR - Natural-Resource Fraction Remaining [].
    ci : numpy.ndarray
        CI - Capital Investment [capital units]. It is a state variable.
    cir : numpy.ndarray
        CIR - Capital-Investment Ratio [capital units/person].
    cig : numpy.ndarray
        CIG - Capital-Investment Generation [capital units/year].
    cid : numpy.ndarray
        CID - Capital-Investment Discard [capital units/year].
    cira : numpy.ndarray
        CIRA - Capital-Investment Ratio in Agriculture [capital units/person].
    ciafn : float
        CIAFN - Capital-Investment-Ratio-in-Agriculture Fraction Normal [].
    msl : numpy.ndarray
        MSL - Material Standard of Living [].
    ecir : numpy.ndarray
        ECIR - Effective-Capital-Investment Ratio [capital units/person].
    ecirn : float
        ECIRN - Effective-Capital-Investment Ratio Normal [capital units/person].
    ciaf : numpy.ndarray
        CIAF - Capital-Investment-in-Agriculture Fraction [].
    ciaft : float
        CIAFT - Capital-Investment-in-Agriculture-Fraction Adjustment Time
        [years].
    fr : numpy.ndarray
        FR - Food Ratio [].
    fn : float
        FN - Food Normal [food units/person/year].
    pol : numpy.ndarray
        POL - Pollution [pollution units].
    polr : numpy.ndarray
        POLR - Pollution Ratio [].
    polg : numpy.ndarray
        POLG - Pollution Generation [pollution units/year].
    pola : numpy.ndarray
        POLA - Pollution Absorption [pollution units/year].
    pols : float
        POLS - Pollution Standard [pollution units].
    ql : numpy.ndarray
        QL - Quality of Life [satisfaction units].
    qls : numpy.ndarray
        QLS - Quality-of-Life Standard [satisfaction units]
    pi : float
        PI - Population, Initial [people].
    nri : float
        NRI - Natural Resources, Initial [natural resources units].
    cii : float
        CII - Capital Investment, Initial [capital units].
    poli : float
        POLI - Pollution, Initial [pollution units].
    ciafi : float
        CIAFI - Capital-Investment-in-Agriculture Fraction, Initial [].
    brcm : interp1d
        BRCM - Birth-Rate-From-Crowding Multiplier [].
    brfm : interp1d
        BRFM - Birth-Rate-From-Food Multiplier [].
    brmm : interp1d
        BRMM - Birth-Rate-From-Material Multiplier [].
    brpm : interp1d
        BRPM - Death-Rate-From-Pollution Multiplier [].
    drcm : interp1d
        DRCM - Death-Rate-From-Crowding Multiplier [].
    drfm : interp1d
        DRFM - Death-Rate-From-Frood Multiplier [].
    drmm : interp1d
        DRMM - Death-Rate-From-Material Multiplier [].
    drpm : interp1d
        DRPM - Death-Rate-From-Pollution Multiplier [].
    cfifr : interp1d
        CFIFR - Capital Fraction Indicated by Food Ratio [].
    cim: interp1d
        CIM - Capital-Investment Multiplier [].
    ciqr : interp1d
        CIQR - Capital-Investment-From-Quality Ratio [].
    fcm : interp1d
        FCM - Food-From-Crowding Multiplier [].
    fpci: interp1d
        FPCI - Food Potential From Capital Investment [food units/person/year].
    fpm : interp1d
        FPM - Food-From-Pollution Multiplier [].
    nrem : interp1d
        NREM - Natural-Resource-Exctraction Multiplier [].
    nrmm : interp1d
        NRMM - Natural-Resource-From-Material Multiplier [].
    polat : interp1d
        POLAT - Pollution-Absoption Time [years].
    polcm : interp1d
        POLCM - Pollution-From-Capital Multiplier [].
    qlc : interp1d
        QLC - Quality of Life from Crowding [].
    qlf : interp1d
        QLF - Quality of Life from Food [].
    qlm : interp1d
        QLM - Quality of Life from Material [].
    qlp : interp1d
        QLP - Quality of Life from Pollution [].
    brn : Clipper
        BRN - Birth Rate Normal [fraction/year].
    drn : Clipper
        DRN - Death Rate Normal [fraction/year].
    cidn : Clipper
        CIDN - Capital-Investment Discard Normal [fraction/year].
    cign : Clipper
        CIGN - Capital-Investment Generation Normal [fraction/year].
    fc : Clipper
        FC - Food Coefficient [].
    nrun : Clipper
        NRUN - Natural-Resource Usage Normal
        [natural resource units/person/year].
    poln : Clipper
        POLN - Pollution Normal [pollution units/person/year].

    """

    def __init__(self, year_min=1900, year_max=2100, dt=0.2):
        """
        __init__ of class World2.

        Parameters
        ----------
        year_min : int, optional
            starting year of the simulation. The default is 1900.
        year_max : int, optional
            end year of the simulation. The default is 2100.
        dt : float, optional
            time step of the numerica integration [year]. The default is 0.2.

        """
        self.year_min = year_min
        self.year_max = year_max
        self.dt = dt
        self.time = np.arange(self.year_min, self.year_max + self.dt, self.dt)
        self.n = self.time.size

    def set_state_variables(self, la=135e6, pdn=26.5, ciafn=0.3, ecirn=1,
                            ciaft=15, pols=3.6e9, fn=1, qls=1):
        """
        Sets constant variables and initializes model vectors.

        Parameters
        ----------
        la : float, optional
            LA - Land Area [square kilometers]. The default is 135e6.
        pdn : float, optional
            PDN - Population Density Normal [people/square kilometer]. The
            default is 26.5.
        ciafn : float, optional
            CIAFN - Capital Investment Ratio in Agriculture Fraction Normal [].
            The default is 0.3.
        ecirn : float, optional
            ECIRN - Effective-Capital-Investment Ratio Normal
            [capital units/person]. The default is 1.
        ciaft : float, optional
            CIAFT - Capital-Investment-in-Agriculture Fraction Adjustment Time
            [years]. The default is 15.
        pols : float, optional
            POLS - Pollution Standard [pollution units]. The default is 3.6e9.
        fn : float, optional
            FN - Food Normal [food units/person/year]. The default is 1.
        qls : float, optional
            QLS - Quality-of-Life Standard [satisfaction units]. The default
            is 1.

        """
        # Variables & constants related to Population
        self.p = np.zeros((self.n,))
        self.br = np.zeros((self.n,))
        self.dr = np.zeros((self.n,))
        self.cr = np.zeros((self.n,))
        self.la = la
        self.pdn = pdn

        # Variables & constants related to Natural Resources
        self.nr = np.zeros((self.n,))
        self.nrur = np.zeros((self.n,))
        self.nrfr = np.zeros((self.n,))

        # Variables & constants related to Capital investsment
        self.ci = np.zeros((self.n,))
        self.cir = np.zeros((self.n,))
        self.cig = np.zeros((self.n,))
        self.cid = np.zeros((self.n,))
        self.cira = np.zeros((self.n,))
        self.ciafn = ciafn

        self.msl = np.zeros((self.n,))
        self.ecir = np.zeros((self.n,))
        self.ecirn = ecirn

        # Variables & constants related to Agriculture & Food
        self.ciaf = np.zeros((self.n,))
        self.ciaft = ciaft
        self.fr = np.zeros((self.n,))
        self.fn = fn

        # Variables & constants related to Pollution
        self.pol = np.zeros((self.n,))
        self.polr = np.zeros((self.n,))
        self.polg = np.zeros((self.n,))
        self.pola = np.zeros((self.n,))
        self.pols = pols

        # Variables & constants related to Quality of Life
        self.ql = np.zeros((self.n,))
        self.qls = qls

    def set_initial_state(self, pi=1.65e9, nri=900e9,
                          cii=0.4e9, poli=0.2e9, ciafi=0.2):
        """
        Sets initial conditions of the state variables.

        Parameters
        ----------
        pi : float, optional
            PI - Population, Initial [people]. The default is 1.65e9.
        nri : float, optional
            NRI - Natural Resources, Initial [natural resources units]. The
            default is 900e9.
        cii : float, optional
            CII - Capital Investment, Initial [capital units]. The default is
            0.4e9.
        poli : float, optional
            POLI - Pollution, Initial [pollution units]. The default is 0.2e9.
        ciafi : float, optional
            CIAFI - Capital-Investment-in-Agriculture Fraction, Initial []. The
            default is 0.2.

        """
        self.pi = pi
        self.nri = nri
        self.cii = cii
        self.poli = poli
        self.ciafi = ciafi

    def set_switch_functions(self, json_file=None):
        """
        Sets all time-dependant variables switched at some threshold year.
        These variables are useful to simulate control policies.

        Parameters
        ----------
        json_file : str, optional
            path to a json configuration file, keeping the same structure as
            "functions_switch_default.json" in pyworld2 library. If None,
            default json file is loaded.

        """
        if json_file is None:
            json_file = "functions_switch_default.json"
            json_file = os.path.join(os.path.dirname(__file__), json_file)
        with open(json_file) as fjson:
            tables = json.load(fjson)

        func_names = ["BRN", "DRN", "CIDN", "CIGN", "FC", "NRUN", "POLN"]

        for func_name in func_names:
            for table in tables:
                if func_name in table:
                    func = Clipper(table[func_name], table[f"{func_name}1"],
                                   table["trigger.value"])
                    setattr(self, func_name.lower(), func)

    def set_table_functions(self, json_file=None):
        """
        Sets all variables dependant on non-linear functions. Output values are
        a linear interpolation of tables.

        Parameters
        ----------
        json_file : str, optional
            path to a json configuration file, keeping the same structure as
            "functions_table_default.json" in pyworld2 library. If None,
            default json file is loaded.

        """
        if json_file is None:
            json_file = "functions_table_default.json"
            json_file = os.path.join(os.path.dirname(__file__), json_file)
        with open(json_file) as fjson:
            tables = json.load(fjson)

        func_names = ["BRCM", "BRFM", "BRMM", "BRPM",
                      "DRCM", "DRFM", "DRMM", "DRPM",
                      "CFIFR", "CIM", "CIQR", "FCM", "FPCI", "FPM",
                      "NREM", "NRMM", "POLAT", "POLCM", "POLR",
                      "QLC", "QLF", "QLM", "QLP"]

        for func_name in func_names:
            for table in tables:
                if table["y.name"] == func_name:
                    func = interp1d(table["x.values"], table["y.values"],
                                    bounds_error=False,
                                    fill_value=(table["y.values"][0],
                                                table["y.values"][-1]))
                    setattr(self, func_name.lower(), func)

    def set_all_standard(self):
        """
        Helper to set everything for a standard run.

        """
        self.set_state_variables()
        self.set_initial_state()
        self.set_table_functions()
        self.set_switch_functions()

    def run(self):
        """
        Runs the simulation.

        """
        self.step_init()
        for k in range(1, self.n):
            self.step(k)

    def step_init(self):
        """
        Runs the simulation at first time step.

        """
        # initialize population
        self.p[0] = self.pi
        self.br[0] = np.nan
        self.dr[0] = np.nan

        # initialize natural resources
        self.nr[0] = self.nri
        self.nrfr[0] = self.nri / self.nri

        # initialize capital investment
        self.ci[0] = self.cii
        self.cr[0] = self.pi / (self.la * self.pdn)
        self.cir[0] = self.cii / self.pi

        # initialize pollution
        self.pol[0] = self.poli
        self.polg[0] = (self.pi * self.poln(self.time[0]) *
                        self.polcm(self.cir[0]))
        self.polr[0] = self.poli / self.pols
        self.pola[0] = self.poli / self.polat(self.polr[0])

        # initialize capital investment in agriculutre fraction
        self.ciaf[0] = self.ciafi
        self.cid[0] = np.nan
        self.cig[0] = np.nan

        # initialize other intermediary variables
        self.cira[0] = self.cir[0] * self.ciafi / self.ciafn
        self.fr[0] = (self.fpci(self.cira[0]) * self.fcm(self.cr[0]) *
                      self.fpm(self.polr[0]) * self.fc(self.time[0])) / self.fn
        self.ecir[0] = (self.cir[0] * (1 - self.ciaf[0]) *
                        self.nrem(self.nrfr[0])) / (1 - self.ciafn)
        self.msl[0] = self.ecir[0] / self.ecirn
        self.ql[0] = np.nan

    def step(self, k):
        """
        Runs the simulation at k-th time step.

        """
        j = k - 1

        # update population state variable
        self.br[k] = (self.p[j] * self.brn(self.time[j]) *
                      self.brmm(self.msl[j]) * self.brcm(self.cr[j]) *
                      self.brfm(self.fr[j]) * self.brpm(self.polr[j]))
        self.dr[k] = (self.p[j] * self.drn(self.time[j]) *
                      self.drmm(self.msl[j]) * self.drpm(self.polr[j]) *
                      self.drfm(self.fr[j]) * self.drcm(self.cr[j]))
        self.p[k] = self.p[j] + (self.br[k] - self.dr[k]) * self.dt

        # update natural resources state variable
        self.nrur[k] = (self.p[j] * self.nrun(self.time[j]) *
                        self.nrmm(self.msl[j]))
        self.nr[k] = self.nr[j] - self.nrur[k] * self.dt
        self.nrfr[k] = self.nr[k] / self.nri

        # update capital investment state variable
        self.cid[k] = self.ci[j] * self.cidn(self.time[j])
        self.cig[k] = (self.p[j] * self.cim(self.msl[j]) *
                       self.cign(self.time[j]))
        # (24):
        self.ci[k] = self.ci[j] + self.dt * (self.cig[k] - self.cid[k])
        self.cr[k] = self.p[k] / (self.la * self.pdn)
        self.cir[k] = self.ci[k] / self.p[k]

        # update pollution state variable
        self.polg[k] = (self.p[j] * self.poln(self.time[j]) *
                        self.polcm(self.cir[j]))
        self.pola[k] = self.pol[j] / self.polat(self.polr[j])
        self.pol[k] = self.pol[j] + (self.polg[k] - self.pola[k]) * self.dt
        self.polr[k] = self.pol[k] / self.pols

        # update capital investment in agriculutre fraction state variable
        self.ciaf[k] = (self.ciaf[j] +
                        (self.cfifr(self.fr[j]) *
                         self.ciqr(self.qlm(self.msl[j]) /
                                   self.qlf(self.fr[j])) -
                         self.ciaf[j]) *
                        (self.dt / self.ciaft))

        # update other intermediary variables
        self.cira[k] = self.cir[k] * self.ciaf[k] / self.ciafn
        self.fr[k] = (self.fcm(self.cr[k]) *
                      self.fpci(self.cira[k]) *
                      self.fpm(self.polr[k]) *
                      self.fc(self.time[k])) / self.fn
        self.ecir[k] = (self.cir[k] *
                        (1 - self.ciaf[k]) *
                        self.nrem(self.nrfr[k])) / (1 - self.ciafn)
        self.msl[k] = self.ecir[k] / self.ecirn
        self.ql[k] = (self.qls * self.qlm(self.msl[k]) *
                      self.qlc(self.cr[k]) * self.qlf(self.fr[k]) *
                      self.qlp(self.polr[k]))


def hello_world2():
    """
    This example runs and plots the 2 scenarios from the book World Dynamics
    by Jay W. Forrester:

        - standard run (Business as usual)

        - reduced usage of Natural Resources.

    """
    # scenario: standard run
    w2_std = World2()
    w2_std.set_state_variables()
    w2_std.set_initial_state()
    w2_std.set_table_functions()
    w2_std.set_switch_functions()
    w2_std.run()

    # scenario: Reduced Usage if Natural Resource
    w2_nr = World2()
    w2_nr.set_state_variables()
    w2_nr.set_initial_state()
    w2_nr.set_table_functions()
    fname_nr = "./functions_switch_scenario_nr.json"
    json_file = os.path.join(os.path.dirname(__file__), fname_nr)
    w2_nr.set_switch_functions(json_file)
    w2_nr.run()

    # plotting
    title_std = "World2 scenario - standard run"
    plot_world_state(w2_std, title=title_std)
    title_nr = "World2 scenario - reduced usage of Natural Resources"
    plot_world_state(w2_nr, title=title_nr)


if __name__ == "__main__":
    hello_world2()
