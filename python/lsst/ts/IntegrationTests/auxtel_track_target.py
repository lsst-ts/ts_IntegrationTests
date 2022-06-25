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

__all__ = ["AuxTelTrackTarget", "run_auxtel_track_target"]

import yaml
import asyncio
import argparse

from lsst.ts.IntegrationTests import BaseScript
from .configs.config_registry import registry


class AuxTelTrackTarget(BaseScript):
    """Execute the given Standard or External script,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    """

    index: int = 2
    configs: tuple = ()
    scripts: list = [
        ("auxtel/track_target.py", BaseScript.is_standard),
    ]

    def __init__(self, target: str) -> None:
        super().__init__()
        self.target_config = yaml.safe_load(registry["track_target"])
        self.target_config["target_name"] = target
        self.configs = (yaml.safe_dump(self.target_config),)


def run_auxtel_track_target() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=str, help="Specify the target to track.")
    args = parser.parse_args()
    script_class = AuxTelTrackTarget(target=args.target)
    num_scripts = len(script_class.scripts)
    print(
        f"\nAuxTel Track Target; running {num_scripts} scripts "
        f"for target configuration:\n{script_class.configs[0]}"
    )
    asyncio.run(script_class.run())
