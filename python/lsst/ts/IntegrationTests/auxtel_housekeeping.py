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

__all__ = ["AuxTelHousekeeping", "run_auxtel_housekeeping"]

import asyncio

from lsst.ts.IntegrationTests import BaseScript

from .configs.config_registry import registry


class AuxTelHousekeeping(BaseScript):
    """Execute the run_command script for the given CSC,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    """

    index: int = 2
    configs: tuple = (
        "",
        registry["atdome_home"],
        registry["atdome_park"],
        registry["atptg_park"],
        registry["atptg_stop_tracking"],
        registry["atmcs_housekeeping"],
    )
    scripts: list = [
        ("auxtel/enable_atcs.py", BaseScript.is_standard),
        ("run_command.py", BaseScript.is_standard),
        ("auxtel/atdome/slew_dome.py", BaseScript.is_standard),
        ("auxtel/point_azel.py", BaseScript.is_standard),
        ("run_command.py", BaseScript.is_standard),
        ("run_command.py", BaseScript.is_standard),
    ]

    def __init__(self) -> None:
        super().__init__()


def run_auxtel_housekeeping() -> None:
    script_class = AuxTelHousekeeping()
    num_scripts = len(script_class.scripts)
    print(f"\nAuxTel Housekeeping; running {num_scripts} scripts")
    asyncio.run(script_class.run())
