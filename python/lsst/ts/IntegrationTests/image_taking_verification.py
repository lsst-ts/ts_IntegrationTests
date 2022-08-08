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

__all__ = [
    "AuxTelImageTaking",
    "ComCamImageTaking",
    "run_auxtel_image_taking",
    "run_comcam_image_taking",
]

import asyncio
from lsst.ts.IntegrationTests import BaseScript
from .configs.config_registry import registry


class AuxTelImageTaking(BaseScript):
    """Execute the given Standard or External script,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    """

    index: int = 2
    configs: tuple = (registry["image_taking"],)
    scripts: list = [
        ("auxtel/take_image_latiss.py", BaseScript.is_standard),
    ]

    def __init__(self) -> None:
        super().__init__()


class ComCamImageTaking(BaseScript):
    """Execute the given Standard or External script,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    """

    index: int = 1
    configs: tuple = (registry["image_taking"],)
    scripts: list = [
        ("maintel/take_image_comcam.py", BaseScript.is_standard),
    ]

    def __init__(self) -> None:
        super().__init__()


def run_auxtel_image_taking() -> None:
    script_class = AuxTelImageTaking()
    num_scripts = len(script_class.scripts)
    print(f"\nAuxTel Image Taking Verification; running {num_scripts} scripts")
    asyncio.run(script_class.run())


def run_comcam_image_taking() -> None:
    script_class = ComCamImageTaking()
    num_scripts = len(script_class.scripts)
    print(f"\nComCam Image Taking Verification; running {num_scripts} scripts")
    asyncio.run(script_class.run())
