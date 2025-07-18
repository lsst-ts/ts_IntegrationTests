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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from base_test import BaseTestClass
from lsst.ts.IntegrationTests import (
    ComCamHousekeeping,
    LsstCamHousekeeping,
    MainTelHousekeeping,
)


class MainTelHousekeepingTestCase(BaseTestClass):
    """Test the MainTel Housekeeping integration test script."""

    # Use MainTel ScriptQueue.
    index = 1

    async def test_comcamhousekeeping(self) -> None:
        """Execute the ComCamHousekeeping integration test script,
        which runs the ts_standardscripts/run_command.py script.

        """
        # Instantiate the ComCamHousekeeping integration tests.
        script_class = ComCamHousekeeping()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"ComCam Housekeeping; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()

    async def test_lsstcamhousekeeping(self) -> None:
        """Execute the LSSTCamHousekeeping integration test script,
        which runs the ts_standardscripts/run_command.py script.

        """
        # Instantiate the LsstCamHousekeeping integration tests.
        script_class = LsstCamHousekeeping()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"LSSTCam Housekeeping; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()

    async def test_maintel_housekeeping(self) -> None:
        """Execute the MainTelHousekeeping integration test script,
        which runs the ts_standardscripts/run_command.py script.

        """
        # Instantiate the MainTelHousekeeping integration tests.
        script_class = MainTelHousekeeping()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"MainTel Housekeeping; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8, 8, 8])
