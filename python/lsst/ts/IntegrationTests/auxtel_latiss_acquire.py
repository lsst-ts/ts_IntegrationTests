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
    "AuxTelLatissAcquire",
    "run_auxtel_latiss_acquire",
]

import argparse
import asyncio

from lsst.ts.IntegrationTests import BaseScript

from .configs.config_registry import registry


class AuxTelLatissAcquire(BaseScript):
    """Execute the given Standard or External script,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    Parameters
    ----------
    sequence : `str`
        Defines which sequence to run.
        Choices are ["verify", "nominal", "test"].
    """

    index: int = 2
    configs: tuple = ([],)
    scripts: list = [
        ("auxtel/latiss_acquire.py", BaseScript.is_external),
    ]

    def __init__(self, sequence: str) -> None:
        super().__init__()
        self.sequence = sequence
        self.configs = (registry[f"auxtel_acquire_{sequence}"],)


def run_auxtel_latiss_acquire() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "sequence",
        type=str,
        choices=["verify", "nominal", "test"],
        help="Specify which sequence to run.",
    )
    args = parser.parse_args()
    script_class = AuxTelLatissAcquire(sequence=args.sequence)
    print(
        f"\nAuxTel Latiss Acquire; "
        f"running the {script_class.scripts[0][0]} script, "
        f"for the {script_class.sequence} sequence, "
        f"with configuration;\n{script_class.configs}"
    )
    asyncio.run(script_class.run())
