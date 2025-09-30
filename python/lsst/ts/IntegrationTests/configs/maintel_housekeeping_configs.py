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

# CCCamera Housekeeping configs
yaml_string = yaml.safe_load(
    """
    component: "CCCamera"
    cmd: "setFilter"
    parameters:
        name: "r_03"
        timeout: 45
    """
)

registry["cccamera_set_filter"] = yaml.safe_dump(
    yaml_string,
    explicit_start=True,
    canonical=True,
)

# MTCamera Housekeeping configs
yaml_string = yaml.safe_load(
    """
    component: "MTCamera"
    cmd: "setFilter"
    parameters:
        name: "r_57"
        timeout: 150
    """
)

registry["mtcamera_set_filter"] = yaml.safe_dump(
    yaml_string,
    explicit_start=True,
    canonical=True,
)

# MTMount Housekeeping configs
yaml_string = yaml.safe_load(
    """
    component: "MTMount"
    cmd: "homeBothAxes"
    """
)

registry["mtmount_home_both_axes"] = yaml.safe_dump(
    yaml_string,
    explicit_start=True,
    canonical=True,
)

# MTPtg park
yaml_string = yaml.safe_load(
    """
    az: 0.0
    el: 80
    target_name: "Park position"
    ignore:
    - mtm1m3
    """
)

registry["mtptg_park"] = yaml.safe_dump(
    yaml_string,
    explicit_start=True,
    canonical=True,
)

# MTPtg stop tracking
yaml_string = yaml.safe_load(
    """
    component: "MTPtg"
    cmd: stopTracking
    """
)

registry["mtptg_stop_tracking"] = yaml.safe_dump(
    yaml_string,
    explicit_start=True,
    canonical=True,
)
