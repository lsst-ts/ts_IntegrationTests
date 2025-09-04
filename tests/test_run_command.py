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
from lsst.ts.IntegrationTests import RunCommand


class RunCommandTestCase(BaseTestClass):
    """Test the Run Command integration test script."""

    async def test_command_no_parameters(self) -> None:
        """Execute a command that does not require parameters."""
        # Instantiate the RunCommand integration test.
        script_class = RunCommand(
            sq_index=1, csc="MTAirCompressor:2", command="powerOn"
        )
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print("Executing MTAirCompressor:2 powerOn command.")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])

    async def test_command_with_string_parameter(self) -> None:
        """Execute a command that requires string parameters."""
        # Instantiate the RunCommand integration test.
        script_class = RunCommand(
            sq_index=1, csc="ATAOS", command="resetOffset", parameters="axis:all"
        )
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print("Executing ATAOS resetOffset command.")
        # Execute the scripts.
        await script_class.run()
        print("assert")
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])

    async def test_command_with_boolean_parameter(self) -> None:
        """Execute a command that requires Boolean parameters."""
        # Instantiate the RunCommand integration test.
        script_class = RunCommand(
            sq_index=1,
            csc="ATAOS",
            command="enableCorrection",
            parameters="enableAll:True",
        )
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print("Executing ATAOS enableCorrection command.")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])

    async def test_command_with_float_parameter(self) -> None:
        """Execute a command that requires float parameters."""
        # Instantiate the RunCommand integration test.
        script_class = RunCommand(
            sq_index=1,
            csc="DIMM:1",
            command="moveDome",
            parameters="sideA:0.4,sideB:0.75",
        )
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print("Executing DIMM:2 moveDome command.")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])

    async def test_command_with_integer_parameter(self) -> None:
        """Execute a command that requires integer parameters."""
        # Instantiate the RunCommand integration test.
        script_class = RunCommand(
            sq_index=1,
            csc="MTCamera",
            command="setFilter",
            parameters="name:r_57,timeout:150",
        )
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print("Executing MTCamera setFilter command.")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])

    async def test_command_with_mixed_parameters(self) -> None:
        """Execute a command that requires multiple types of parameters."""
        # Instantiate the RunCommand integration test.
        script_class = RunCommand(
            sq_index=1,
            csc="Test",
            command="setScalars",
            parameters="boolean0:False,int0:42,float0:47.5,string0:Peekaboo",
        )
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print("Executing MTCamera setFilter command.")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])
