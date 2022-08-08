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
from parameterized import parameterized

from lsst.ts import salobj
from lsst.ts.IntegrationTests import ScriptQueueController
from lsst.ts.IntegrationTests import AuxTelLatissCWFSAlign
from lsst.ts.IntegrationTests import AuxTelLatissAcquireTakeSequence


class AuxTelNightOperationsTestCase(unittest.IsolatedAsyncioTestCase):
    """
    Test the AuxTel Night Operations integration test scripts.
    """

    async def asyncSetUp(self) -> None:
        # Set the LSST_DDS_PARTITION_PREFIX ENV_VAR.
        salobj.set_random_lsst_dds_partition_prefix()

        # Create the ScriptQueue Controller.
        self.controller = ScriptQueueController(index=2)

        # Start the controller and wait for it be ready.
        await self.controller.start_task

    async def test_auxtel_latiss_cwfs_align(self) -> None:
        """Execute the AuxTelLatissCWFSAlign integration test script,
        which runs the ts_standardscripts/auxtel/make_latiss_cwfs_align.py
        script.
        Use the configuration stored in the auxtel_night_operations_configs.py
        module.
        """
        # Instantiate the AuxTelLatissCWFSAlign integration tests object and
        # execute the scripts.
        script_class = AuxTelLatissCWFSAlign()
        await script_class.run()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(
            f"AuxTel Latiss CWFS Align. "
            f"Running the {script_class.scripts[0][0]} script,"
            f"\nwith configuration;\n{script_class.configs}"
        )
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)

    @parameterized.expand(["pointing", "verify", "nominal", "test"])
    async def test_auxtel_latiss_acquire_and_take_sequence(self, sequence: str) -> None:
        """Execute the AuxTelLatissAcquireTakeSequence integration test script,
        which runs the
        ts_standardscripts/auxtel/auxtel_latiss_acquire_and_take_sequence.py
        script.
        Use the configurations stored in the auxtel_night_operations_configs.py
        module.
        """
        # Instantiate the AuxTelLatissAcquireTakeSequence integration tests
        # objectand execute the scripts.
        script_class = AuxTelLatissAcquireTakeSequence(sequence=sequence)
        await script_class.run()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(
            f"AuxTel Latiss Acquire and Take Sequence. "
            f"Running the {script_class.scripts[0][0]} script, "
            f"for the {script_class.sequence} sequence, "
            f"\nwith configuration;\n{script_class.configs}"
        )
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
