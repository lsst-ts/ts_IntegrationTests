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

__all__ = ["AuxTelResetOffsets", "run_auxtel_reset_offsets"]

import asyncio

from lsst.ts.IntegrationTests import BaseScript

from .configs.config_registry import registry


class AuxTelResetOffsets(BaseScript):
    """Execute the run_command script for the given CSC,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    """

    index: int = 2
    configs: tuple = (
        registry["auxtel_enable_all_corrections"],
        registry["auxtel_reset_offsets"],
        registry["auxtel_disable_all_corrections"],
        registry["auxtel_enable_m1_hex_atspect_corrections"],
    )
    scripts: list = [
        ("run_command.py", BaseScript.is_standard),
        ("run_command.py", BaseScript.is_standard),
        ("run_command.py", BaseScript.is_standard),
        ("run_command.py", BaseScript.is_standard),
    ]

    def __init__(self) -> None:
        super().__init__()


def run_auxtel_reset_offsets() -> None:
    script_class = AuxTelResetOffsets()
    num_scripts = len(script_class.scripts)
    print(f"\nAuxTel Reset Offsets; running {num_scripts} scripts")
    asyncio.run(script_class.run())
