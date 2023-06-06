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

import unittest

from lsst.ts import salobj
from lsst.ts.IntegrationTests import (
    MainTelDisabledEnabled,
    MainTelOfflineStandby,
    MainTelStandbyDisabled,
    ScriptQueueController,
)


class MainTelStateTransitionTestCase(unittest.IsolatedAsyncioTestCase):
    """Test the MainTel Standby to Disabled integration test script."""

    async def asyncSetUp(self) -> None:
        # Set the LSST_DDS_PARTITION_PREFIX ENV_VAR.
        salobj.set_random_lsst_dds_partition_prefix()

        # Create the ScriptQueue Controller.
        self.controller = ScriptQueueController(index=1)

        # Start the controller and wait for it be ready.
        await self.controller.start_task

    async def test_maintel_offline_standby(self) -> None:
        """Execute the MainTelOfflineStandby integration test script,
        which runs the ts_standardscripts/set_summary_state.py script.
        Use the configuration stored in the at_state_transition_configs.py
        module.

        """
        # Instantiate the MainTelOfflineStandby integration tests.
        script_class = MainTelOfflineStandby()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"MainTel Offline to Standby; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])

    async def test_maintel_standby_disabled(self) -> None:
        """Execute the MainTelStandbyDisabled integration test script,
        which runs the ts_standardscripts/set_summary_state.py script.
        Use the configuration stored in the at_state_transition_configs.py
        module.

        """
        # Instantiate the MainTelStandbyDisabled integration tests.
        script_class = MainTelStandbyDisabled()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"MainTel Standby to Disabled; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8, 8])

    async def test_maintel_disabled_enabled(self) -> None:
        """Execute the MainTelDisabledEnabled integration test script,
        which runs the ts_standardscripts/set_summary_state.py script.
        Use the configuration stored in the at_state_transition_configs.py
        module.

        """
        # Instantiate the MainTelDisabledEnabled integration tests.
        script_class = MainTelDisabledEnabled()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"MainTel Disabled to Enabled; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8, 8])

    async def asyncTearDown(self) -> None:
        await self.controller.close()
        await self.controller.done_task
