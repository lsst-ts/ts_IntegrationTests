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

__all__ = ["MainTelLaserTrackerAlign", "maintel_lasertracker_align"]

import argparse
import asyncio

import yaml
from lsst.ts.IntegrationTests import BaseScript


class MainTelLaserTrackerAlign(BaseScript):
    """Execute the maintel/laser_tracker/align.py standard script.

    Attributes
    ----------
    target : `string`
        Name of the target to align against.
        One of ["Camera", "M2", "CALIBRATION_SCREEN"].
    """

    index: int = 1
    configs: tuple = ("",)
    scripts: list = [
        ("maintel/laser_tracker/align.py", BaseScript.is_standard),
    ]

    def __init__(
        self,
        target: str,
    ) -> None:
        super().__init__()
        self.target = target
        # Convert config to a properly formatted YAML document.
        yaml_string = yaml.safe_load(f"""
            target: {self.target}
            program: "Integration testing."
            reason: "Integration testing."
            """)
        self.configs = (
            yaml.safe_dump(yaml_string, explicit_start=True, canonical=True),
        )


def maintel_lasertracker_align() -> None:
    # Define the script arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "target",
        metavar="target",
        type=str,
        choices=["Camera", "M2", "CALIBRATION_SCREEN"],
        help="Specify the target to align against.",
    )
    args = parser.parse_args()
    main(args)


def main(opts: argparse.Namespace) -> None:
    # Ensure the invocation is correct.
    # If not, raise KeyError.
    # If it is correct, execute the slew.
    try:
        script_class = MainTelLaserTrackerAlign(
            target=opts.target,
        )
    except KeyError as ke:
        print(repr(ke))
    else:
        print(f"Align the LaserTracker to the {script_class.target}.")
        asyncio.run(script_class.run())
