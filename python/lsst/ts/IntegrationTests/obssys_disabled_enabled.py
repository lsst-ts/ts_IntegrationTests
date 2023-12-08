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

__all__ = ["ObsSysDisabledEnabled", "run_obssys_disabled_enabled"]

import asyncio

import yaml
from lsst.ts.IntegrationTests import BaseScript

from .configs.config_registry import registry
from .utils import get_test_env_arg


class ObsSysDisabledEnabled(BaseScript):
    """Execute the given Standard or External script,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    """

    index: int = 1
    configs: tuple = (registry["obssys_disabled_enabled"],)
    scripts: list = [
        ("set_summary_state.py", BaseScript.is_standard),
    ]

    def __init__(self, test_env: str) -> None:
        super().__init__()
        # Set the OCPS index based on test environment
        self.test_env = test_env
        self.env_configs = yaml.safe_load(registry["obssys_disabled_enabled"])
        if test_env.lower() == "bts":
            # Running on BTS with OCPS:3
            self.ocps = "OCPS:3"
        else:
            # Running on TTS or Summit with OCPS:2
            self.ocps = "OCPS:2"
        self.env_configs["data"][-1][0] = self.ocps
        self.configs = (yaml.safe_dump(self.env_configs),)


def run_obssys_disabled_enabled() -> None:
    # Ensure the invocation is correct.
    # If not, raise KeyError.
    # If it is correct, execute the state transition.
    args = get_test_env_arg()
    try:
        script_class = ObsSysDisabledEnabled(
            test_env=args.test_env,
        )
    except KeyError as ke:
        print(repr(ke))
    else:
        num_scripts = len(script_class.scripts)
        print(
            f"\nObsSys Disabled to Enabled; "
            f"running {num_scripts} scripts "
            f"on the '{args.test_env}' environment, "
            f"with this configuration: \n"
            f"{script_class.configs}"
        )
        asyncio.run(script_class.run())
