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

__all__ = ["MainTelSlewDome", "maintel_slew_dome"]

import argparse
import asyncio
from typing import List

import yaml
from lsst.ts.IntegrationTests import BaseScript


class MainTelSlewDome(BaseScript):
    """Execute the maintel/mtdome/slew_dome.py standard script.

    Attributes
    ----------
    az : `float`
        The azimuth position of the slew.
    ignore : `List[str]`
        A list of CSCs to ignore when executing the slew.
        Default is [] (empty list).
    """

    configs: tuple = ()
    scripts: list = [
        ("maintel/mtdome/slew_dome.py", BaseScript.is_standard),
    ]

    def __init__(self, az: float, ignore: List[str] = []) -> None:
        super().__init__()
        self.az = az
        self.ignore = ignore
        # Convert config to a properly formatted YAML document.
        yaml_string = yaml.safe_load(
            f"""
            az: {self.az}
            ignore: {self.ignore}
            """
        )
        self.configs = (
            yaml.safe_dump(yaml_string, explicit_start=True, canonical=True),
        )


def maintel_slew_dome() -> None:
    # Define the script arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "az",
        metavar="Azimuth",
        type=float,
        help="Specify the desired Azimuth position.",
    )
    parser.add_argument(
        "-i",
        "--ignore",
        metavar="Ignore",
        type=str,
        nargs="*",
        default=[],
        help="Specify the list of CSCs for the command to ignore.",
    )
    args = parser.parse_args()
    main(args)


def main(opts: argparse.Namespace) -> None:
    # Ensure the invocation is correct.
    # If not, raise KeyError.
    # If it is correct, execute the slew.
    try:
        script_class = MainTelSlewDome(
            az=opts.az,
            ignore=opts.ignore,
        )
    except KeyError as ke:
        print(repr(ke))
    else:
        print(
            f"\nSlewing MTDome to {opts.az} degrees." f"\nIgnore list: {opts.ignore}."
        )
        asyncio.run(script_class.run())
