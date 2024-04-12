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

# eas_standby_disabled
yaml_string = yaml.safe_load(
    """
    data:
    - [DIMM:1, DISABLED]
    - [DIMM:2, DISABLED]
    - [ESS:1, DISABLED]
    - [ESS:101, DISABLED]
    - [ESS:102, DISABLED]
    - [ESS:103, DISABLED]
    - [ESS:104, DISABLED]
    - [ESS:105, DISABLED]
    - [ESS:106, DISABLED]
    - [ESS:201, DISABLED]
    - [ESS:202, DISABLED]
    - [ESS:203, DISABLED]
    - [ESS:204, DISABLED]
    - [ESS:205, DISABLED]
    - [ESS:301, DISABLED]
    """
)

registry["eas_standby_disabled"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)

# eas_disabled_enabled
yaml_string = yaml.safe_load(
    """
    data:
    - [DIMM:1, ENABLED]
    - [DIMM:2, ENABLED]
    - [ESS:1, ENABLED]
    - [ESS:101, ENABLED]
    - [ESS:102, ENABLED]
    - [ESS:103, ENABLED]
    - [ESS:104, ENABLED]
    - [ESS:105, ENABLED]
    - [ESS:106, ENABLED]
    - [ESS:201, ENABLED]
    - [ESS:202, ENABLED]
    - [ESS:203, ENABLED]
    - [ESS:204, ENABLED]
    - [ESS:205, ENABLED]
    - [ESS:301, ENABLED]
    """
)

registry["eas_disabled_enabled"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)
