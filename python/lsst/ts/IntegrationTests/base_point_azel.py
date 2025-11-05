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
    "BasePointAzEl",
]

import argparse

from lsst.ts.IntegrationTests import BaseScript


class BasePointAzEl(BaseScript):
    """Base script that defines pointing the telescope
    to a fixed Az/El/Rot position. Execute with the given Yaml
    configuration, placed in the given ScriptQueue location.

    Attributes
    ----------
    az : `float`
        The commanded azimuth position.
    el : `float`
        The commanded elevation position.
    rot_tel: `float`
        Rotator angle in mount physical coordinates (degrees).
        default: 0.0
    target_name: `str`
        Name of the position.
        default: "AzEl"
    ignore : `List[str]`
        A list of CSCs to ignore when executing the command.
    """

    def __init__(self, args=None) -> None:
        super().__init__()
        self.parser = argparse.ArgumentParser(
            description="Base class for telescope pointing."
        )
        # Define the script arguments.
        self.parser.add_argument(
            "az",
            metavar="Azimuth",
            type=float,
            help="Specify the desired Azimuth position.",
        )
        self.parser.add_argument(
            "el",
            metavar="Elevation",
            type=float,
            help="Specify the desired Elevation position.",
        )
        self.parser.add_argument(
            "-r",
            "--rot_tel",
            metavar="RotatorAngle",
            type=float,
            default=0.0,
            help="Specify the desired Rotator angle in mount physical coordinates (degrees).",
        )
        self.parser.add_argument(
            "-t",
            "--target_name",
            metavar="TargetName",
            type=str,
            default="AzEl",
            help="Specify the name of the target in plain speech.",
        )
        self.parser.add_argument(
            "-i",
            "--ignore",
            metavar="Ignore",
            type=str,
            nargs="*",
            default=[],
            help="Specify the list of CSCs for the command to ignore.",
        )
        self.args = self.parser.parse_args(args)
