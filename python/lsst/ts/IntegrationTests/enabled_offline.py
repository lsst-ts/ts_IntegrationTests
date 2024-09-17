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

__all__ = ["EnabledOffline", "run_enabled_offline"]

import asyncio

from lsst.ts.IntegrationTests import BaseScript

from .configs.config_registry import registry


class EnabledOffline(BaseScript):
    """Execute the given Standard or External script,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    """

    index: int = 2
    configs: tuple = (
        registry["watcher_enabled_offline"],
        registry["sched_ocps_enabled_offline"],
        "",
        "",
        registry["mtcs_enabled_offline"],
        registry["eas_enabled_offline"],
        registry["maintel_enabled_offline"],
        registry["gencam_enabled_offline"],
        # The ScriptQueue script must run last.
        registry["sq_enabled_offline"],
    )
    scripts: list = [
        ("set_summary_state.py", BaseScript.is_standard),
        ("set_summary_state.py", BaseScript.is_standard),
        ("auxtel/offline_atcs.py", BaseScript.is_standard),
        ("auxtel/offline_latiss.py", BaseScript.is_standard),
        ("maintel/offline_mtcs.py", BaseScript.is_standard),
        ("set_summary_state.py", BaseScript.is_standard),
        ("set_summary_state.py", BaseScript.is_standard),
        ("set_summary_state.py", BaseScript.is_standard),
        ("set_summary_state.py", BaseScript.is_standard),
    ]

    def __init__(self) -> None:
        super().__init__()


def run_enabled_offline() -> None:
    # Ensure the invocation is correct.
    # If not, raise KeyError.
    # If it is correct, execute the state transition.
    try:
        script_class = EnabledOffline()
    except KeyError as ke:
        print(repr(ke))
    else:
        num_scripts = len(script_class.scripts)
        print(
            f"\nEnabled to Offline; "
            f"running {num_scripts} scripts "
            f"with this configuration: \n"
            f"{script_class.configs}"
        )
        asyncio.run(script_class.run())
