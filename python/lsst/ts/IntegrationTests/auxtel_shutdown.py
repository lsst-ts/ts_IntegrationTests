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

__all__ = ["AuxTelShutdown", "run_auxtel_shutdown"]

import asyncio
from lsst.ts.IntegrationTests import BaseScript


class AuxTelShutdown(BaseScript):
    """Execute the given Standard or External script,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    """

    index: int = 2
    configs: tuple = ([], [])
    scripts: list = [
        ("auxtel/shutdown.py", BaseScript.is_standard),
        ("auxtel/enable_atcs.py", BaseScript.is_standard),
    ]

    def __init__(self) -> None:
        super().__init__()


def run_auxtel_shutdown() -> None:
    script_class = AuxTelShutdown()
    num_scripts = len(script_class.scripts)
    print(f"\nAuxTel Shutdown; running {num_scripts} scripts")
    asyncio.run(script_class.run())
