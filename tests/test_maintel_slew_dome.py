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
from lsst.ts.IntegrationTests import MainTelSlewDome


class MainTelSlewDomeTestCase(BaseTestClass):
    """
    Test the MainTel Point AzEl integration test scripts.
    """

    # Use MainTel ScriptQueue.
    index = 1

    async def test_maintel_slew_dome(self) -> None:
        """Execute the MainTelSlewDome integration test script,
        which runs the standard/maintel/slew_dome.py
        script.
        """
        # Instantiate the MainTelSlewDome integration tests.
        script_class = MainTelSlewDome(az=328)
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(
            f"MainTel SlewDome. "
            f"Running the {script_class.scripts[0][0]} script."
            f"\nAzimuth coords: [{script_class.az}]"
            f"\nIgnore list: {script_class.ignore}"
        )
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])
        # Assert script arguments are correct.
        self.assertEqual(script_class.az, float(328))
        self.assertEqual(script_class.ignore, [])

    async def test_maintel_slew_dome_ignore_list(self) -> None:
        """Execute the MainTelSlewDome integration test script,
        which runs the standard/maintel/slew_dome.py
        script.
        Test the ignore list.
        """
        # Instantiate the MainTelSlewDome integration tests.
        script_class = MainTelSlewDome(
            az=0,
            ignore="mtm1m3,mtm2,mtaos,mthexapod_1,mthexapod_2,mtmount,mtptg,mtrotator",
        )
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(
            f"MainTel SlewDome. "
            f"Running the {script_class.scripts[0][0]} script."
            f"\nAzimuth coords: [{script_class.az}]"
            f"\nIgnore list: {script_class.ignore}"
        )
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])
        # Assert script arguments are correct.
        self.assertEqual(script_class.az, float(0))
        self.assertEqual(
            script_class.ignore,
            "mtm1m3,mtm2,mtaos,mthexapod_1,mthexapod_2,mtmount,mtptg,mtrotator",
        )

    async def test_maintel_slew_dome_no_args(self) -> None:
        """Execute the MainTelSlewDome integration test script,
        which runs the standard/maintel/slew_dome.py
        script.
        Leave cli arguments blank. Should fail.
        """
        # Instantiate the MainTelSlewDome integration tests with no arguments.
        with self.assertRaises(TypeError):
            MainTelSlewDome()
