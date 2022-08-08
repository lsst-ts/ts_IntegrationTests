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
from lsst.ts.IntegrationTests import AuxTelPrepareFlat


class AuxTelPrepareFlatTestCase(unittest.IsolatedAsyncioTestCase):
    """Test the AuxTel PrepareFlat integration test script."""

    async def asyncSetUp(self) -> None:
        # Set the LSST_DDS_PARTITION_PREFIX ENV_VAR.
        salobj.set_random_lsst_dds_partition_prefix()

        # Create the ScriptQueue Controller.
        self.controller = ScriptQueueController(index=2)

        # Start the controller and wait for it be ready.
        await self.controller.start_task

    async def test_auxtel_prepare_flat(self) -> None:
        """Execute the AuxTelPrepareFlat integration test script,
        which runs the ts_standardscripts/auxtel/prepare_for_flat.py
        script.
        This test requires no configuration.

        """
        # Instantiate the AuxTelPrepareFlat integration tests object and
        # execute the scripts.
        script_class = AuxTelPrepareFlat()
        await script_class.run()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"AuxTel Prepare for Flat; running {num_scripts} scripts")
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)

    async def asyncTearDown(self) -> None:
        await self.controller.close()
        await self.controller.done_task
