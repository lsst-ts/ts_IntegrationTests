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

__all__ = ["AuxTelLatissCalibrations", "run_auxtel_latiss_calibrations"]

import yaml
import asyncio
import argparse

from lsst.ts.IntegrationTests import BaseScript
from .configs.config_registry import registry


class AuxTelLatissCalibrations(BaseScript):
    """Execute the given Standard or External script,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    Parameters
    ----------
    calib_type : `str`
        Defines which set of calibrations to run.
        Choices are ["flat", "ptc"].
    """

    index: int = 2
    configs: tuple = ([],)
    scripts: list = [
        ("auxtel/make_latiss_calibrations.py", BaseScript.is_standard),
    ]

    def __init__(self, calib_type: str) -> None:
        super().__init__()
        self.calib_type = calib_type
        self.calib_configs = yaml.safe_load(
            registry[f"latiss_calibrations_{calib_type}"]
        )
        self.calib_configs["certify_calib_begin_date"] = super().get_current_date()
        self.calib_configs["calib_collection"] = self.calib_configs[
            "calib_collection"
        ].replace("replace_me", super().get_current_date("%Y%m%d"))
        self.calib_configs["calib_collection"] = self.calib_configs[
            "calib_collection"
        ].replace("calib_type", calib_type)
        self.configs = (yaml.safe_dump(self.calib_configs),)


def run_auxtel_latiss_calibrations() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--calib_type",
        "-t",
        type=str,
        choices=["flat", "ptc"],
        required=True,
        help="Specify which set of calibrations to run.",
    )
    args = parser.parse_args()
    script_class = AuxTelLatissCalibrations(calib_type=args.calib_type)
    print(
        f"\nAuxTel Make Latiss Calibrations; running the master_{script_class.calib_type} calibrations,"
        f"\nwith configuration;\n{script_class.configs}"
    )
    asyncio.run(script_class.run())
