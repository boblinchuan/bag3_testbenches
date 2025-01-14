# BSD 3-Clause License
#
# Copyright (c) 2018, Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from typing import Any, Optional, Mapping, List, Union, Dict

from bag.simulation.data import SimNetlistInfo, netlist_info_from_dict

from ..base import GenericTB


class PSSTB(GenericTB):
    """This class provide utility methods useful for all PSS simulations.

    Notes
    -----
    specification dictionary has the following optional entries in addition to the default ones:

    p_port/n_port : str/str
        p_port and n_port in autonomous circuit (e.g. free-running VCO)
    fund: Union[float, str]
        Steady state analysis fundamental frequency (or its estimate for autonomous circuits).
    period : Union[float, str]
        Steady state analysis period (or its estimate for autonomous circuits).
    autofund: bool
        If the value is yes, the program ignores period/fund value and calculates
        the fundamental frequency automatically from source information.
    t_step : Optional[float]
        Optional.  The strobe period.  Defaults to no strobing.
    pss_options : Mapping[str, Any]
        PSS simulation options dictionary. (spectre -h pss to see available parameters)
    """

    def get_pss_sim_setup(self) -> Dict[str, Any]:
        specs = self.specs
        t_step: Optional[float] = specs.get('t_step', None)
        pss_options: Mapping[str, Any] = specs.get('pss_options', {})

        pss_dict = dict(type='PSS',
                        options=pss_options,
                        save_outputs=self.save_outputs,
                        )
        if t_step is not None:
            pss_dict['strobe'] = t_step

        for optional_key in ['p_port', 'n_port', 'period', 'fund', 'autofund']:
            if optional_key in specs:
                pss_dict[optional_key] = specs[optional_key]
        sim_setup = self.get_netlist_info_dict()
        sim_setup['analyses'] = [pss_dict]
        return sim_setup

    def get_netlist_info(self) -> SimNetlistInfo:
        sim_setup = self.get_pss_sim_setup()
        return netlist_info_from_dict(sim_setup)

