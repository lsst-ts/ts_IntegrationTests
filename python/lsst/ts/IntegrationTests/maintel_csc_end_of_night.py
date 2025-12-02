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

__all__ = ["MainTelCscEndOfNight", "maintel_csc_end_of_night"]

import argparse
import asyncio
from typing import List

import yaml
from lsst.ts.IntegrationTests import BaseScript


class MainTelCscEndOfNight(BaseScript):
    """Execute the maintel/csc_end_of_night.py standard script.

    Attributes
    ----------
    ignore : `List[str]`
        A list of CSCs to ignore when executing the end-of-night script.
        Default is [] (empty list).
    """

    configs: tuple = ()
    scripts: list = [
        ("maintel/csc_end_of_night.py", BaseScript.is_standard),
    ]

    def __init__(self, ignore: List[str] = []) -> None:
        super().__init__()
        self.ignore = ignore
        # Convert config to a properly formatted YAML document.
        yaml_string = yaml.safe_load(
            f"""
            ignore: {self.ignore}
            """
        )
        self.configs = (
            yaml.safe_dump(yaml_string, explicit_start=True, canonical=True),
        )


def maintel_csc_end_of_night() -> None:
    # Define the script arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--ignore",
        metavar="Ignore",
        type=str,
        nargs="*",
        default=[],
        help="Specify the list of CSCs for the script to ignore.",
    )
    args = parser.parse_args()
    main(args)


def main(opts: argparse.Namespace) -> None:
    # Ensure the invocation is correct.
    # If not, raise KeyError.
    # If it is correct, execute the end-of-night script.
    try:
        script_class = MainTelCscEndOfNight(
            ignore=opts.ignore,
        )
    except KeyError as ke:
        print(repr(ke))
    else:
        print(f"\nExecuting End-of-Night activities." f"\nIgnore list: {opts.ignore}.")
        asyncio.run(script_class.run())
