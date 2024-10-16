# SPDX-License-Identifier: Apache-2.0
# Copyright 2019 Blue Cheetah Analog Design Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Optional, Mapping

from bag.simulation.data import SimNetlistInfo, netlist_info_from_dict

from ..base import GenericTB


class TranTB(GenericTB):
    """This class provide utility methods useful for all transient simulations.

    Notes
    -----
    specification dictionary has the following entries in addition to the default ones:

    sim_params : Mapping[str, float]
        Required entries are listed below.

        t_sim : float
            the total simulation time.

    subclasses can define the following optional entries:

    t_step : Optional[float]
        Optional.  The strobe period.  Defaults to no strobing.
    t_start : Optional[float]
        Optional.  The simulation start time. Defaults to 0.
        If negative and a ramp-up option is selected to compute initial conditions, the ramp-up duration is -t_start.
    tran_options : Mapping[str, Any]
        Optional.  transient simulation options dictionary.
    """

    def get_netlist_info(self) -> SimNetlistInfo:
        specs = self.specs
        t_step: Optional[float] = specs.get('t_step', None)
        tran_options: Mapping[str, Any] = specs.get('tran_options', {})
        sweep_var: str = specs.get('sweep_var', None)
        sweep_options: Mapping[str, Any] = specs.get('sweep_options', None)

        tran_dict = dict(type='TRAN',
                         start=specs.get('t_start', 0.0),
                         stop='t_sim',
                         options=tran_options,
                         save_outputs=self.save_outputs,
                         )
        if sweep_var and sweep_options:
            tran_dict['sweep_var'] = sweep_var
            tran_dict['sweep_options'] = sweep_options
        if t_step is not None:
            tran_dict['strobe'] = t_step

        sim_setup = self.get_netlist_info_dict()
        sim_setup['analyses'] = [tran_dict]
        sim_setup['init_voltages'] = specs.get('ic', {})
        return netlist_info_from_dict(sim_setup)
