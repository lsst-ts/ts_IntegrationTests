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
from lsst.ts.IntegrationTests import GenCamDisabledEnabled, GenCamStandbyDisabled


class GenCamStateTransitionTestCase(BaseTestClass):
    """Test the GenCam Standby to Disabled integration test script."""

    # Use OCS ScriptQueue.
    index = 3

    async def test_gencam_standby_disabled(self) -> None:
        """Execute the GenCamStandbyDisabled integration test script,
        which runs the ts_standardscripts/set_summary_state.py script.
        Use the configuration stored in the gencam_state_transition_configs.py
        module.

        """
        # Instantiate the GenCamStandbyDisabled integration tests.
        script_class = GenCamStandbyDisabled()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"GenCam Standby to Disabled; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])

    async def test_gencam_disabled_enabled(self) -> None:
        """Execute the GenCamDisabledEnabled integration test script,
        which runs the ts_standardscripts/set_summary_state.py script.
        Use the configuration stored in the gencam_state_transition_configs.py
        module.

        """
        # Instantiate the GenCamDisabledEnabled integration tests.
        script_class = GenCamDisabledEnabled()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"GenCam Disabled to Enabled; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])
