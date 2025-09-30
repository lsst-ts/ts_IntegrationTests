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

__all__ = [
    "ComCamHousekeeping",
    "LsstCamHousekeeping",
    "MainTelHousekeeping",
    "run_comcam_housekeeping",
    "run_lsstcam_housekeeping",
    "run_maintel_housekeeping",
]

import asyncio

from lsst.ts.IntegrationTests import BaseScript

from .configs.config_registry import registry


class ComCamHousekeeping(BaseScript):
    """Execute the run_command script for the given CSC,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    """

    index: int = 1
    configs: tuple = (registry["cccamera_set_filter"],)
    scripts: list = [
        ("run_command.py", BaseScript.is_standard),
    ]

    def __init__(self) -> None:
        super().__init__()


class LsstCamHousekeeping(BaseScript):
    """Execute the run_command script for the given CSC,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    """

    index: int = 1
    configs: tuple = (registry["mtcamera_set_filter"],)
    scripts: list = [
        ("run_command.py", BaseScript.is_standard),
    ]

    def __init__(self) -> None:
        super().__init__()


class MainTelHousekeeping(BaseScript):
    """Execute the run_command script for the given CSC,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    """

    index: int = 1
    configs: tuple = (
        registry["mtmount_home_both_axes"],
        registry["mtptg_park"],
        registry["mtptg_stop_tracking"],
    )
    scripts: list = [
        ("run_command.py", BaseScript.is_standard),
        ("maintel/point_azel.py", BaseScript.is_standard),
        ("run_command.py", BaseScript.is_standard),
    ]

    def __init__(self) -> None:
        super().__init__()


def run_comcam_housekeeping() -> None:
    script_class = ComCamHousekeeping()
    num_scripts = len(script_class.scripts)
    print(f"\nComCam Housekeeping; running {num_scripts} scripts")
    asyncio.run(script_class.run())


def run_lsstcam_housekeeping() -> None:
    script_class = LsstCamHousekeeping()
    num_scripts = len(script_class.scripts)
    print(f"\nLSSTCam Housekeeping; running {num_scripts} scripts")
    asyncio.run(script_class.run())


def run_maintel_housekeeping() -> None:
    script_class = MainTelHousekeeping()
    num_scripts = len(script_class.scripts)
    print(f"\nMainTel Housekeeping; running {num_scripts} scripts")
    asyncio.run(script_class.run())
