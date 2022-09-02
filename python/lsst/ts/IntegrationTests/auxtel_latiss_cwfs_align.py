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

__all__ = ["AuxTelLatissCWFSAlign", "run_auxtel_latiss_cwfs_align"]

import asyncio

from lsst.ts.IntegrationTests import BaseScript
from .configs.config_registry import registry


class AuxTelLatissCWFSAlign(BaseScript):
    """Execute the given Standard or External script,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.
    """

    index: int = 2
    configs: tuple = (registry["auxtel_cwfs_align"],)
    scripts: list = [
        ("auxtel/latiss_cwfs_align.py", BaseScript.is_external),
    ]

    def __init__(self) -> None:
        super().__init__()


def run_auxtel_latiss_cwfs_align() -> None:
    script_class = AuxTelLatissCWFSAlign()
    print(
        f"\nAuxTel Latiss CWFS Align; running the {script_class.scripts[0][0]} script,"
        f"\nwith configuration;\n{script_class.configs}"
    )
    asyncio.run(script_class.run())
