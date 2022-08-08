# This file is part of ts_IntegrationTests
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
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
    "AuxTelLatissAcquireTakeSequence",
    "run_auxtel_latiss_acquire_and_take_sequence",
]

import asyncio
import argparse

from lsst.ts.IntegrationTests import BaseScript
from .configs.config_registry import registry


class AuxTelLatissAcquireTakeSequence(BaseScript):
    """Execute the given Standard or External script,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    Parameters
    ----------
    sequence : `str`
        Defines which sequence to run.
        Choices are ["pointing", "verify", "nominal", "test"].
    """

    index: int = 2
    configs: tuple = ([],)
    scripts: list = [
        ("auxtel/latiss_acquire_and_take_sequence.py", BaseScript.is_standard),
    ]

    def __init__(self, sequence: str) -> None:
        super().__init__()
        self.sequence = sequence
        self.configs = (registry[f"auxtel_acquire_and_take_sequence_{sequence}"],)


def run_auxtel_latiss_acquire_and_take_sequence() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sequence",
        "-s",
        type=str,
        choices=["pointing", "verify", "nominal", "test"],
        required=True,
        help="Specify which sequence to run.",
    )
    args = parser.parse_args()
    script_class = AuxTelLatissAcquireTakeSequence(sequence=args.sequence)
    print(
        f"\nAuxTel Latiss Acquire and Take Sequence; "
        f"running the {script_class.scripts[0][0]} script, "
        f"for the {script_class.sequence} sequence, "
        f"with configuration;\n{script_class.configs}"
    )
    asyncio.run(script_class.run())
