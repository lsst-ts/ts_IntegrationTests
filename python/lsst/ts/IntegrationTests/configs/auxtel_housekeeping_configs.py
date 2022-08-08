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


# Add the script configurations to the configuration registry.

# ATMCS Housekeeping configs
yaml_string = yaml.safe_load(
    """
    component: "ATMCS"
    cmd: "setInstrumentPort"
    parameters:
        port: 7
    """
)

registry["atmcs_housekeeping"] = yaml.safe_dump(
    yaml_string,
    explicit_start=True,
    canonical=True,
)

# ATSpectrograph Housekeeping configs
yaml_string = yaml.safe_load(
    """
    component: "ATSpectrograph"
    cmd: "changeDisperser"
    parameters:
        name: "empty_1"
    """
)

registry["atspectrograph_housekeeping"] = yaml.safe_dump(
    yaml_string,
    explicit_start=True,
    canonical=True,
)
