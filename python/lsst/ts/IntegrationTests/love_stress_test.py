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

__all__ = ["LoveStressTest", "run_love_stress_test"]

import asyncio

import yaml
from lsst.ts.IntegrationTests import BaseScript

from .configs.config_registry import registry
from .utils import get_test_env_arg


class LoveStressTest(BaseScript):
    """Execute the given Standard or External script,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    Attributes
    ----------
    test_env : `str`
        Defines which test environment the script is running.
        Choices are ['bts', 'tts', 'summit'].
    k8s : `bool`
        Indicates if the script should run against the kubernetes
        instance. Default is False.
    """

    index: int = 1
    configs: tuple = (registry["love_stress"],)
    scripts: list = [
        ("make_love_stress_tests.py", BaseScript.is_external),
    ]

    def __init__(self, test_env: str, k8s: bool = False) -> None:
        super().__init__()
        # Set the LOVE location based on test environment
        self.test_env = test_env
        self.k8s = k8s
        self.env_configs = yaml.safe_load(registry["love_stress"])
        if test_env.lower() == "summit":
            # Running on Summit
            if self.k8s:
                self.location = "https://summit-lsp.lsst.codes/love"
            else:
                self.location = "http://love01.cp.lsst.org"
        elif test_env.lower() == "tts":
            # Running on TTS
            if self.k8s:
                self.location = "https://tucson-teststand.lsst.codes/love"
            else:
                self.location = "http://love1.tu.lsst.org"
        elif test_env.lower() == "bts":
            # Running on BTS
            if self.k8s:
                self.location = "https://base-lsp.lsst.codes/love"
            else:
                self.location = "http://love01.ls.lsst.org"
        else:
            raise Exception(
                "Please choose one of the proper locations: ['bts', 'tts', 'summit']"
            )
        self.env_configs["location"] = self.location
        self.configs = (yaml.safe_dump(self.env_configs),)


def run_love_stress_test() -> None:
    # Ensure the invocation is correct.
    # If not, raise KeyError.
    # If it is correct, execute the Stress Test.
    args = get_test_env_arg()
    try:
        script_class = LoveStressTest(
            test_env=args.test_env,
            k8s=args.k8s,
        )
    except KeyError as ke:
        print(repr(ke))
    else:
        num_scripts = len(script_class.scripts)
        print(
            f"\nLOVE Stress Test; running {num_scripts} scripts"
            f" with this configuration:\n"
            f"{script_class.configs}"
        )
        asyncio.run(script_class.run())
