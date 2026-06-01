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
from lsst.ts.IntegrationTests import MainTelRaiseM1M3


class MainTelRaiseM1M3TestCase(BaseTestClass):
    """
    Test the MainTel RaiseM1M3 integration test scripts.
    """

    # Use MainTel ScriptQueue.
    index = 1

    async def test_maintel_raise_m1m3(self) -> None:
        """Execute the MainTelRaiseM1M3 integration test script,
        which runs the maintel/m1m3/raise_m1m3.py
        standard script.
        """
        # Instantiate the MainTelRaiseM1M3 integration tests.
        script_class = MainTelRaiseM1M3()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(
            f"Test MainTel RaiseM1M3.\nRunning the {script_class.scripts[0][0]} script."
        )
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])
