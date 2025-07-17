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
    AuxTelDisabledEnabled,
    AuxTelOfflineStandby,
    AuxTelStandbyDisabled,
    ScriptQueueController,
)


class AuxTelStateTransitionTestCase(unittest.IsolatedAsyncioTestCase):
    """Test the AuxTel Standby to Disabled integration test script."""

    async def asyncSetUp(self) -> None:
        # Define LSST_TOPIC_SUBNAME.
        salobj.set_test_topic_subname()

        # Create the ScriptQueue Controller.
        self.controller = ScriptQueueController(index=2)

        # Start the controller and wait for it be ready.
        await self.controller.start_task

    async def test_auxtel_offline_standby(self) -> None:
        """Execute the AuxTelOfflineStandby integration test script,
        which runs the ts_standardscripts/set_summary_state.py script.
        Use the configuration stored in the at_state_transition_configs.py
        module.

        """
        # Instantiate the AuxTelOfflineStandby integration tests.
        script_class = AuxTelOfflineStandby()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"AuxTel Offline to Standby; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])

    async def test_auxtel_standby_disabled(self) -> None:
        """Execute the AuxTelStandbyDisabled integration test script,
        which runs the ts_standardscripts/set_summary_state.py script.
        Use the configuration stored in the at_state_transition_configs.py
        module.

        """
        # Instantiate the AuxTelStandbyEnabled integration tests.
        script_class = AuxTelStandbyDisabled()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"AuxTel Standby to Disabled; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8, 8])

    async def test_auxtel_disabled_enabled(self) -> None:
        """Execute the AuxTelDisabledEnabled integration test script,
        which runs the ts_standardscripts/set_summary_state.py script.
        Use the configuration stored in the at_state_transition_configs.py
        module.
        """
        # Instantiate the AuxTelDisabledEnabled integration tests.
        script_class = AuxTelDisabledEnabled()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"AuxTel Disabled to Enabled; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8, 8])
