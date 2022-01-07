# This file is part of ts_IntegrationTests
#
# Developed for the LSST Telescope and Site Systems.
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

__all__ = ["AuxTelShutdown"]

from lsst.ts.IntegrationTests import BaseScript
from .config_registry import registry


class AuxTelShutdown(BaseScript):
    """Execute the given Auxilliary Telescope Standard or External
    script, with the given Yaml configuration, placed in the
    given ScriptQueue location.

    """

    index = 2
    configs = ([], registry["enable1"])

    scripts = (
        "auxtel/shutdown.py",
        "auxtel/enable_atcs.py",
    )

    def __init__(self, isStandard=True, queue_placement="after"):
        super().__init__(
            isStandard=isStandard,
            queue_placement=queue_placement,
        )