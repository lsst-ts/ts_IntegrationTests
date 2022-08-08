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

# obssys2_standby_disabled
yaml_string = yaml.safe_load(
    """
    data:
    - [Scheduler:1, DISABLED]
    - [Scheduler:2, DISABLED]
    - [OCPS:1, DISABLED]
    - [OCPS:2, DISABLED]
    """
)

registry["obssys2_standby_disabled"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)

# obssys2_disabled_enabled
yaml_string = yaml.safe_load(
    """
    data:
    - [Scheduler:1, ENABLED]
    - [Scheduler:2, ENABLED]
    - [OCPS:1, ENABLED]
    - [OCPS:2, ENABLED]
    """
)

registry["obssys2_disabled_enabled"] = yaml.safe_dump(
    yaml_string, explicit_start=True, canonical=True
)
