#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of ts_IntegrationTests.
#
# Developed for the Vera C. Rubin Observatory Telescope & Site Software system.
# This product includes software developed by the Vera C. Rubin Observatory
# Project (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import yaml

from .config_registry import registry

# Add the script configurations to the configuration registry.

# ATDome homed config
yaml_string = yaml.safe_load(
    """
    component: "ATDome"
    cmd: "homeAzimuth"
    """
)

registry["atdome_home"] = yaml.safe_dump(
    yaml_string,
    explicit_start=True,
    canonical=True,
)

# ATDome park configs
yaml_string = yaml.safe_load(
    """
    component: "ATDome"
    cmd: moveAzimuth
    parameters:
        azimuth: 285
    """
)

registry["atdome_park"] = yaml.safe_dump(
    yaml_string,
    explicit_start=True,
    canonical=True,
)

# ATMCS setInstrumentPort configs
yaml_string = yaml.safe_load(
    """
    component: "ATMCS"
    cmd: "setInstrumentPort"
    parameters:
        port: 2
    """
)

registry["atmcs_housekeeping"] = yaml.safe_dump(
    yaml_string,
    explicit_start=True,
    canonical=True,
)
