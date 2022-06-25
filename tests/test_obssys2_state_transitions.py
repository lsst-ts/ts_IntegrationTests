#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of ts_IntegrationTests.
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import unittest

from lsst.ts import salobj
from lsst.ts.IntegrationTests import ScriptQueueController
from lsst.ts.IntegrationTests import ObsSys2StandbyDisabled
from lsst.ts.IntegrationTests import ObsSys2DisabledEnabled


class ObsSys2StateTransitionTestCase(unittest.IsolatedAsyncioTestCase):
    """Test the ObsSys2 Standby to Disabled integration test script."""

    async def asyncSetUp(self) -> None:
        # Set the LSST_DDS_PARTITION_PREFIX ENV_VAR.
        salobj.set_random_lsst_dds_partition_prefix()

        # Create the ScriptQueue Controller.
        self.controller = ScriptQueueController(index=1)

        # Start the controller and wait for it be ready.
        await self.controller.start_task

    async def test_obssys2_standby_disabled(self) -> None:
        """Execute the ObsSys2StandbyDisabled integration test script,
        which runs the ts_standardscripts/set_summary_state.py script.
        Use the configuration stored in the obssys2_state_transition_configs.py
        module.

        """
        # Instantiate the ObsSys2StandbyDisabled integration tests object and
        # execute the scripts.
        script_class = ObsSys2StandbyDisabled()
        await script_class.run()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"ObsSys2 Standby to Disabled; running {num_scripts} scripts")
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)

    async def test_obssys2_disabled_enabled(self) -> None:
        """Execute the ObsSys2DisabledEnabled integration test script,
        which runs the ts_standardscripts/set_summary_state.py script.
        Use the configuration stored in the obssys2_state_transition_configs.py
        module.

        """
        # Instantiate the ObsSys2DisabledEnabled integration tests object and
        # execute the scripts.
        script_class = ObsSys2DisabledEnabled()
        await script_class.run()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"ObsSys2 Disabled to Enabled; running {num_scripts} scripts")
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)

    async def asyncTearDown(self) -> None:
        await self.controller.close()
        await self.controller.done_task
