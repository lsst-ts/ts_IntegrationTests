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

# auxtel_standby_disabled
yaml_string = yaml.safe_load(
    """
    data:
    - [ATDome, DISABLED]
    - [ATDomeTrajectory, DISABLED]
    - [ATMCS, DISABLED]
    - [ATPneumatics, DISABLED]
    - [ATAOS, DISABLED]
    - [ATHexapod, DISABLED]
    - [ATPtg, DISABLED]
    """
)

registry["auxtel_standby_disabled"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)

# auxtel_camera_standby_disabled
yaml_string = yaml.safe_load(
    """
    data:
    - [ATOODS, DISABLED]
    - [ATCamera, DISABLED, Normal]
    - [ATHeaderService, DISABLED]
    - [ATSpectrograph, DISABLED]
    """
)

registry["auxtel_camera_standby_disabled"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)

# auxtel_disabled_enabled
yaml_string = yaml.safe_load(
    """
    data:
    - [ATDome, ENABLED]
    - [ATDomeTrajectory, ENABLED]
    - [ATMCS, ENABLED]
    - [ATPneumatics, ENABLED]
    - [ATAOS, ENABLED]
    - [ATHexapod, ENABLED]
    - [ATPtg, ENABLED]
    """
)

registry["auxtel_disabled_enabled"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)

# auxtel_camera_disabled_enabled
yaml_string = yaml.safe_load(
    """
    data:
    - [ATOODS, ENABLED]
    - [ATCamera, ENABLED]
    - [ATHeaderService, ENABLED]
    - [ATSpectrograph, ENABLED]
    """
)

registry["auxtel_camera_disabled_enabled"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)

# auxtel_offline_standby
yaml_string = yaml.safe_load(
    """
    data:
    - [ATCamera, STANDBY]
    """
)

registry["auxtel_offline_standby"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)
