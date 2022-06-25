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

__all__ = ["MainTelDisabledEnabled", "run_maintel_disabled_enabled"]

import asyncio
from lsst.ts.IntegrationTests import BaseScript
from .configs.config_registry import registry


class MainTelDisabledEnabled(BaseScript):
    """Execute the given Standard or External script,
    with the given Yaml configuration,
    placed in the given ScriptQueue location.

    """

    index: int = 1
    configs: tuple = (
        registry["maintel_disabled_enabled"],
        registry["mtaircomp_disabled_enabled"],
        registry["maintel_camera_disabled_enabled"],
    )
    scripts: list = [
        ("set_summary_state.py", BaseScript.is_standard),
        ("set_summary_state.py", BaseScript.is_standard),
        ("set_summary_state.py", BaseScript.is_standard),
    ]

    def __init__(self) -> None:
        super().__init__()


def run_maintel_disabled_enabled() -> None:
    script_class = MainTelDisabledEnabled()
    num_scripts = len(script_class.scripts)
    print(f"\nMainTel Disabled to Enabled; running {num_scripts} scripts")
    asyncio.run(script_class.run())
