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

from typing import Any, Sequence, Mapping

from bag.simulation.data import SimNetlistInfo, netlist_info_from_dict

from ..base import GenericTB


class DCTB(GenericTB):
    """This class provide utility methods useful for all dc simulations.

    Notes
    -----
    specification dictionary has the following entries in addition to the default ones:

    sweep_var : str
        The variable to be swept.
    sweep_options : Mapping[str, Any]
        Dictionary with following entries :
            type : str
                type of DC sweep (LINEAR / LOG)
            start : Union[str, float]
                initial value of sweep_var
            stop : Union[str, float]
                final value of sweep_var
            num : int
                number of sweep data points

    subclasses can define the following optional entries:

    dc_options : Mapping[str, Any]
        Optional.  dc simulation options dictionary.
    """

    def get_netlist_info(self) -> SimNetlistInfo:
        specs = self.specs
        sweep_var: str = specs['sweep_var']
        sweep_options: Mapping[str, Any] = specs['sweep_options']
        dc_options: Mapping[str, Any] = specs.get('dc_options', {})
        save_outputs: Sequence[str] = specs.get('save_outputs', [])

        dc_dict = dict(type='DC',
                       param=sweep_var,
                       sweep=sweep_options,
                       options=dc_options,
                       save_outputs=save_outputs,
                       )

        sim_setup = self.get_netlist_info_dict()
        sim_setup['analyses'] = [dc_dict]
        return netlist_info_from_dict(sim_setup)
