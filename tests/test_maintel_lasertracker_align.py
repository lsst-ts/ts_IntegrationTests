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

import subprocess

from base_test import BaseTestClass
from lsst.ts.IntegrationTests import MainTelLaserTrackerAlign


class MainTelLaserTrackerAlignTestCase(BaseTestClass):
    """
    Test the LaserTracker Align integration test scripts.
    """

    # Use MainTel ScriptQueue.
    index = 1

    async def test_lasertracker_align(self) -> None:
        """Execute the MainTelLaserTrackerAlign integration test script,
        which runs the standard/maintel/lasertracker/align.py
        script.
        """
        # Instantiate the MainTelLaserTrackerAlign integration tests.
        args = ["Camera"]
        script_class = MainTelLaserTrackerAlign(args)
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(
            f"LaserTracker Align. "
            f"Running the {script_class.scripts[0][0]} script."
            f"\nTarget: {script_class.target}"
        )
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])
        # Assert script arguments are correct.
        self.assertEqual(script_class.target, args)

    async def test_lasertracker_align_invalid_arg(self) -> None:
        """Execute the MainTelLaserTrackerAlign integration test script,
        which runs the standard/maintel/lasertracker/align.py
        script.
        Attempt to use an invalid argument. Should fail.
        """
        # Instantiate the MainTelLaserTrackerAlign integration tests.
        args = ["maintel_lasertracker_align", "Fail"]
        child_process = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = child_process.communicate()  # type: bytes
        print(f"Result: {stdout}")
        print(f"Error: {stderr}")
        if "invalid choice" in stderr:
            assert True
        else:
            assert False

    async def test_lasertracker_align_no_args(self) -> None:
        """Execute the MainTelLaserTrackerAlign integration test script,
        which runs the standard/maintel/lasertracker/align.py
        script.
        Leave cli arguments blank. Should fail.
        """
        # Instantiate the MainTelLaserTrackerAlign integration tests.
        # Expect a TypeError.
        with self.assertRaises(TypeError):
            MainTelLaserTrackerAlign()
