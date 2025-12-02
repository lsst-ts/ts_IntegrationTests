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
from lsst.ts.IntegrationTests import MainTelCscEndOfNight


class MainTelCscEndOfNightTestCase(BaseTestClass):
    """
    Test the MainTel CSC End-of-Nightintegration test script.
    """

    # Use MainTel ScriptQueue.
    index = 1

    async def test_maintel_csc_end_of_night(self) -> None:
        """Execute the MainTelCscEndOfNight integration test script,
        which runs the standard/maintel/csc_end_of_night.py
        script.
        """
        # Instantiate the MainTelCscEndOfNight integration tests.
        script_class = MainTelCscEndOfNight()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(
            f"MainTel CscEndOfNight. "
            f"Running the {script_class.scripts[0][0]} script."
            f"\nIgnore list: {script_class.ignore}"
        )
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])
        # Assert script arguments are correct.
        self.assertEqual(script_class.ignore, [])

    async def test_maintel_csc_end_of_night_ignore_list(self) -> None:
        """Execute the MainTelCscEndOfNight integration test script,
        which runs the standard/maintel/csc_end_of_night.py
        script.
        Test the ignore list.
        """
        # Instantiate the MainTelCscEndOfNight integration tests.
        script_class = MainTelCscEndOfNight(
            ignore="mtm1m3,mtm2,mtaos,mthexapod_1,mthexapod_2,mtmount,mtptg,mtrotator",
        )
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(
            f"MainTel CscEndOfNight. "
            f"Running the {script_class.scripts[0][0]} script."
            f"\nIgnore list: {script_class.ignore}"
        )
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])
        # Assert script arguments are correct.
        self.assertEqual(
            script_class.ignore,
            "mtm1m3,mtm2,mtaos,mthexapod_1,mthexapod_2,mtmount,mtptg,mtrotator",
        )
