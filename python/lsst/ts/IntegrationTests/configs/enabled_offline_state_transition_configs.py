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

# Add the State Transition script configurations to the registry.

# watcher_enabled_offline
yaml_string = yaml.safe_load(
    """
    data:
    - [Watcher, OFFLINE]
    """
)

registry["watcher_enabled_offline"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)

# sched_ocps_enabled_offline
yaml_string = yaml.safe_load(
    """
    data:
    - [Scheduler:1, OFFLINE]
    - [Scheduler:2, OFFLINE]
    - [OCPS:1, OFFLINE]
    """
)

registry["sched_ocps_enabled_offline"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)

# eas_enabled_offline
yaml_string = yaml.safe_load(
    """
    data:
    - [DSM:2, OFFLINE]
    - [DSM:1, OFFLINE]
    - [DIMM:1, OFFLINE]
    - [DIMM:2, OFFLINE]
    - [ESS:1, OFFLINE]
    - [ESS:101, OFFLINE]
    - [ESS:102, OFFLINE]
    - [ESS:103, OFFLINE]
    - [ESS:104, OFFLINE]
    - [ESS:105, OFFLINE]
    - [ESS:106, OFFLINE]
    - [ESS:201, OFFLINE]
    - [ESS:202, OFFLINE]
    - [ESS:203, OFFLINE]
    - [ESS:204, OFFLINE]
    - [ESS:205, OFFLINE]
    - [ESS:301, OFFLINE]
    - [WeatherForecast, OFFLINE]
    """
)

registry["eas_enabled_offline"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)

# authorize_test42_sq_enabled_offline
yaml_string = yaml.safe_load(
    """
    data:
    - [Authorize, OFFLINE]
    - [Test:42, OFFLINE]
    - [ScriptQueue:1, OFFLINE]
    - [ScriptQueue:2, OFFLINE]
    """
)

registry["sq_enabled_offline"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)

# MainTel enabled_offline
yaml_string = yaml.safe_load(
    """
    data:
    - [MTAirCompressor:1, OFFLINE]
    - [MTAirCompressor:2, OFFLINE]
    - [LaserTracker:1, OFFLINE]
    """
)

registry["maintel_enabled_offline"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)

# MainTel Camera enabled_offline
yaml_string = yaml.safe_load(
    """
    data:
    - [MTHeaderService, OFFLINE]
    - [MTOODS, OFFLINE]
    """
)

registry["maintel_camera_enabled_offline"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)

# GenCam enabled_offline
yaml_string = yaml.safe_load(
    """
    data:
    - [GenericCamera:1, OFFLINE]
    - [GCHeaderService:1, OFFLINE]
    """
)

registry["gencam_enabled_offline"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)
