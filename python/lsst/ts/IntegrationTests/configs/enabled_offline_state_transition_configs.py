# This file is part of ts_IntegrationTests.
#
# Developed for the Rubin Observatory Telescope and Site System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
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

# sched_ocps_enabled_offline
yaml_string = yaml.safe_load(
    """
    data:
    - [Scheduler:1, OFFLINE]
    - [Scheduler:2, OFFLINE]
    - [OCPS:1, OFFLINE]
    - [OCPS:2, OFFLINE]
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
    - [WeatherStation:1, OFFLINE]
    """
)

registry["eas_enabled_offline"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)

# watcher_sq_enabled_offline
yaml_string = yaml.safe_load(
    """
    data:
    - [Watcher, OFFLINE]
    - [ScriptQueue:1, OFFLINE]
    - [ScriptQueue:2, OFFLINE]
    """
)

registry["watcher_sq_enabled_offline"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)

# MTAirCompressor enabled_offline
yaml_string = yaml.safe_load(
    """
    data:
    - [MTAirCompressor:1, OFFLINE]
    - [MTAirCompressor:2, OFFLINE]
    """
)

registry["mtaircomp_enabled_offline"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)
