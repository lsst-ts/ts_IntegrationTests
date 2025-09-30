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
from lsst.ts import salobj
from lsst.ts.IntegrationTests import AuxTelHousekeeping, FailingScriptQueueController


class FailedScriptTestCase(BaseTestClass):
    """Test when a script is FAILED."""

    async def asyncSetUp(self) -> None:
        # Define LSST_TOPIC_SUBNAME.
        salobj.set_test_topic_subname()

        # Create the ScriptQueue Controller.
        self.controller = FailingScriptQueueController(index=2, test_type="FAILED")

        # Start the controller and wait for it be ready.
        await self.controller.start_task

    async def test_failed_script(self) -> None:
        """Execute the AuxTelHousekeeping integration test script,
        but make the final states FAILED.
        """
        # Instantiate the AuxTelHousekeeping integration tests.
        script_class = AuxTelHousekeeping()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"AuxTel Housekeeping; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts are FAILED.
        # When a script is FAILED, it pauses the ScriptQueue and keeps the
        # failed script in the queue. The integration test script handles this
        # by sending a resume command to the SQ. By verifying the final script
        # states, this test ensures the test script doesn't hang and properly
        # processes through the SQ.
        self.assertEqual(script_class.script_states, [10, 10, 10, 10, 10, 10])
