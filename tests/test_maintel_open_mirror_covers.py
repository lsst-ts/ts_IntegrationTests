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
from lsst.ts.IntegrationTests import MainTelOpenMirrorCovers


class MainTelOpenMirrorCoversTestCase(BaseTestClass):
    """
    Test the MainTel OpenMirrorCovers integration test scripts.
    """

    # Use MainTel ScriptQueue.
    index = 1

    async def test_maintel_open_mirror_covers(self) -> None:
        """Execute the MainTelOpenMirrorCovers integration test script,
        which runs the standard/maintel/open_mirror_covers.py
        script.
        """
        # Instantiate the MainTelOpenMirrorCovers integration tests.
        script_class = MainTelOpenMirrorCovers()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(
            f"MainTel OpenMirrorCovers. "
            f"Running the {script_class.scripts[0][0]} script."
        )
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])
        # Assert script arguments are correct.
        self.assertEqual(script_class.ignore, [])

    async def test_maintel_open_mirror_covers_ignore_list(self) -> None:
        """Execute the MainTelOpenMirrorCovers integration test script,
        which runs the standard/maintel/open_mirror_covers.py
        script.
        Test the ignore list.
        """
        # Instantiate the MainTelOpenMirrorCovers integration tests.
        script_class = MainTelOpenMirrorCovers(
            ignore="mtm1m3,mtm2,mtaos,mthexapod_1,mthexapod_2,mtmount,mtptg,mtrotator",
        )
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(
            f"MainTel OpenMirrorCovers. "
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
