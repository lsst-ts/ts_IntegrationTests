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

import yaml
from lsst.ts import salobj
from lsst.ts.IntegrationTests import (
    ObsSysDisabledEnabled,
    ObsSysStandbyDisabled,
    ScriptQueueController,
)


class ObsSysStateTransitionTestCase(unittest.IsolatedAsyncioTestCase):
    """Test the ObsSys Standby to Disabled integration test script."""

    async def asyncSetUp(self) -> None:
        # Set the LSST_DDS_PARTITION_PREFIX ENV_VAR.
        salobj.set_random_lsst_dds_partition_prefix()

        # Create the ScriptQueue Controller.
        self.controller = ScriptQueueController(index=1)

        # Start the controller and wait for it be ready.
        await self.controller.start_task

    async def test_obssys_standby_disabled(self) -> None:
        """Execute the ObsSysStandbyDisabled integration test script,
        which runs the ts_standardscripts/set_summary_state.py script.
        Use the configuration stored in the obssys_state_transition_configs.py
        module.
        """

        # Instantiate the ObsSysStandbyDisabled integration tests.
        script_class = ObsSysStandbyDisabled()
        # Get number of scripts and the configuration.
        num_scripts = len(script_class.scripts)
        script_config = yaml.safe_load(script_class.configs[0])
        print(
            f"ObsSys Standby to Disabled; running {num_scripts} scripts, "
            f"with this configuration: \n"
            f"{script_config}"
        )
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])

    async def test_obssys_disabled_enabled(self) -> None:
        """Execute the ObsSysDisabledEnabled integration test script,
        which runs the ts_standardscripts/set_summary_state.py script.
        Use the configuration stored in the obssys_state_transition_configs.py
        module.
        """

        # Instantiate the ObsSysDisabledEnabled integration tests.
        script_class = ObsSysDisabledEnabled()
        # Get number of scripts and the configuration.
        num_scripts = len(script_class.scripts)
        script_config = yaml.safe_load(script_class.configs[0])
        print(
            f"ObsSys Disabled to Enabled; running {num_scripts} scripts, "
            f"with this configuration: \n"
            f"{script_config}"
        )
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])

    async def asyncTearDown(self) -> None:
        await self.controller.close()
        await self.controller.done_task
