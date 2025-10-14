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
from lsst.ts.IntegrationTests import CSCStateTransition


class CSCStateTransitionTestCase(BaseTestClass):
    """Test the CSC State transition integration test script."""

    # Use MainTel ScriptQueue.
    index = 1

    async def test_comcam_offline_standby(self) -> None:
        """Execute the Offline-to-Standby state transition for ComCam."""
        # Instantiate the CSCStateTransition integration test.
        script_class = CSCStateTransition(
            csc="CCCamera", state="Standby", sq_index=CSCStateTransitionTestCase.index
        )
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"ComCam Offline to Standby; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])

    async def test_lsstcam_offline_standby(self) -> None:
        """Execute the Offline-to-Standby state transition for LSSTCam."""
        # Instantiate the CSCStateTransition integration tests.
        script_class = CSCStateTransition(
            csc="MTCamera", state="Standby", sq_index=CSCStateTransitionTestCase.index
        )
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"LSSTCam Offline to Standby; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])

    async def test_additional_configuration(self) -> None:
        """Verify additional_configuration flag adds miscellaneous configs"""
        # Instantiate the CSCStateTransition integration tests.
        script_class = CSCStateTransition(
            csc="Test",
            state="Offline",
            sq_index=CSCStateTransitionTestCase.index,
            additional_configuration="Normal",
        )
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert script config contains additional config items.
        self.assertEqual(script_class.added_config, "Normal")

    async def test_mute_alarms_flag(self) -> None:
        """Verify mute_alarms flag adds mute_alarms:true to script config"""
        # Instantiate the CSCStateTransition integration tests.
        script_class = CSCStateTransition(
            csc="Test",
            state="Offline",
            sq_index=CSCStateTransitionTestCase.index,
            mute_alarms=True,
        )
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])
        # Assert script config contains mute_alarms:true.
        self.assertEqual(script_class.mute_alarms, True)
