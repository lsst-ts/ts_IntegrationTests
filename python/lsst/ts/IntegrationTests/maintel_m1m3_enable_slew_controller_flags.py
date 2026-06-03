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
    "MainTelM1M3EnableSlewControllerFlags",
    "maintel_m1m3_enable_slew_controller_flags",
]

import asyncio

from lsst.ts.IntegrationTests import BaseScript

from .configs.config_registry import registry


class MainTelM1M3EnableSlewControllerFlags(BaseScript):
    """Execute the maintel/m1m3/enable_m1m3_slew_controller_flags.py
    standard script.
    """

    configs: tuple = registry["m1m3_disable_slew_controller_flags"]
    scripts: list = [
        ("maintel/m1m3/enable_m1m3_slew_controller_flags.py", BaseScript.is_standard),
    ]

    def __init__(self) -> None:
        super().__init__()


def maintel_m1m3_enable_slew_controller_flags() -> None:
    # Ensure the invocation is correct.
    # If not, raise KeyError.
    # If it is correct, execute the raise.
    try:
        script_class = MainTelM1M3EnableSlewControllerFlags()
    except KeyError as ke:
        print(repr(ke))
    else:
        print("\nDisabling M1M3 slew controller flags.")
        asyncio.run(script_class.run())
