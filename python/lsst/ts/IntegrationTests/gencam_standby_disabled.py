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

__all__ = ["GenCamStandbyDisabled", "run_gencam_standby_disabled"]

import asyncio

from lsst.ts.IntegrationTests import BaseScript

from .configs.config_registry import registry


class GenCamStandbyDisabled(BaseScript):
    """Execute the given Standard or External script,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    """

    index: int = 3
    configs: tuple = (registry["gencam_standby_disabled"],)
    scripts: list = [
        ("set_summary_state.py", BaseScript.is_standard),
    ]

    def __init__(self) -> None:
        super().__init__()


def run_gencam_standby_disabled() -> None:
    script_class = GenCamStandbyDisabled()
    num_scripts = len(script_class.scripts)
    print(f"\nGenCam Standby to Disabled; running {num_scripts} scripts")
    asyncio.run(script_class.run())
