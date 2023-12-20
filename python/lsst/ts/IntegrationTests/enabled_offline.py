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

import argparse
import asyncio

import yaml
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
        [],
        [],
        [],
        [],
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
        ("replace_with_big_camera_offline_script", BaseScript.is_standard),
        ("set_summary_state.py", BaseScript.is_standard),
        ("set_summary_state.py", BaseScript.is_standard),
        ("set_summary_state.py", BaseScript.is_standard),
        ("set_summary_state.py", BaseScript.is_standard),
    ]

    def __init__(self, test_env: str) -> None:
        super().__init__()
        # Set the OCPS index based on test environment
        self.test_env = test_env
        self.obssys_configs = yaml.safe_load(self.configs[1])
        if self.test_env.lower() == "bts":
            # Running on BTS with MTCamera and OCPS:3
            self.big_cam_script = "maintel/offline_lsstcam.py"
            self.ocps = "OCPS:3"
        else:
            # Running on TTS or Summit with CCCamera and OCPS:2
            self.big_cam_script = "maintel/offline_comcam.py"
            self.ocps = "OCPS:2"
        self.obssys_configs["data"][3][0] = self.ocps
        # Update the self.configs tuple with the updated
        # registry["sched_ocps_enabled_offline"] configuration.
        # Do this by converting the tuple to a list, replacing the
        # updated entry and converting it back to a tuple.
        self.obssys_configs = yaml.safe_load(self.configs[1])
        temp_list = list(self.configs)
        temp_list[1] = yaml.safe_dump(
            self.obssys_configs, explicit_start=True, canonical=True
        )
        self.configs = tuple(temp_list)
        # Update the self.scripts tuple with the proper Camera
        # shutdown script, based on the environment.
        temp_scripts = list(self.scripts)
        temp_scripts[5] = self.big_cam_script
        self.scripts = tuple(temp_scripts)


def run_enabled_offline() -> None:
    # Define the script arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "test_env",
        nargs="?",
        type=str.lower,
        choices=["bts", "tts", "summit"],
        help="Specify on which environment the tests are running (case insensitive).",
    )
    args = parser.parse_args()
    # Print the help if the environment is not defined.
    if not (args.test_env):
        parser.print_help()
        exit()
    main(args)


def main(opts: argparse.Namespace) -> None:
    # Ensure the invocation is correct.
    # If not, raise KeyError.
    # If it is correct, execute the state transition.
    try:
        script_class = EnabledOffline(
            test_env=opts.test_env,
        )
    except KeyError as ke:
        print(repr(ke))
    else:
        num_scripts = len(script_class.scripts)
        print(
            f"\nEnabled to Offline; "
            f"running {num_scripts} scripts "
            f"on the '{opts.test_env}' environment. "
            f"with this configuration: \n"
            f"{script_class.configs}"
        )
        asyncio.run(script_class.run())
