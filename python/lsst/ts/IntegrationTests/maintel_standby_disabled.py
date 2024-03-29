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

__all__ = ["MainTelStandbyDisabled", "run_maintel_standby_disabled"]

import asyncio

import yaml
from lsst.ts.IntegrationTests import BaseScript

from .configs.config_registry import registry
from .utils import get_test_env_arg


class MainTelStandbyDisabled(BaseScript):
    """Execute the given Standard or External script,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    """

    index: int = 1
    configs: tuple = (
        registry["maintel_standby_disabled"],
        registry["maintel_camera_standby_disabled"],
    )
    scripts: list = [
        ("set_summary_state.py", BaseScript.is_standard),
        ("set_summary_state.py", BaseScript.is_standard),
    ]

    def __init__(self, test_env: str) -> None:
        super().__init__()
        # Set the MainTel Camera based on the test environment.
        self.test_env = test_env
        self.big_cam_configs = yaml.safe_load(
            registry["maintel_camera_standby_disabled"]
        )
        if test_env.lower() == "bts":
            # Running on BTS with MTCamera
            self.big_cam_hs = "MTHeaderService"
            self.big_cam_oods = "MTOODS"
        else:
            # Running on TTS or Summit with CCCamera
            self.big_cam_hs = "CCHeaderService"
            self.big_cam_oods = "CCOODS"
        self.big_cam_configs["data"][0][0] = self.big_cam_hs
        self.big_cam_configs["data"][1][0] = self.big_cam_oods
        self.configs = (
            registry["maintel_standby_disabled"],
            yaml.safe_dump(self.big_cam_configs),
        )


def run_maintel_standby_disabled() -> None:
    # Ensure the invocation is correct.
    # If not, raise KeyError.
    # If it is correct, execute the state transition.
    args = get_test_env_arg()
    try:
        script_class = MainTelStandbyDisabled(
            test_env=args.test_env,
        )
    except KeyError as ke:
        print(repr(ke))
    else:
        num_scripts = len(script_class.scripts)
        print(
            f"\nMainTel Standby to Disabled; "
            f"running {num_scripts} scripts "
            f"on the '{args.test_env}' environment, "
            f"with this configuration: \n"
            f"{script_class.configs}"
        )
        asyncio.run(script_class.run())
