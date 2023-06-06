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
from lsst.ts.IntegrationTests import ScriptQueueController, TelescopeAndDomeCheckout


class TelescopeAndDomeCheckoutTestCase(unittest.IsolatedAsyncioTestCase):
    """Test the AuxTel Telescope and Dome Checkout integration test script."""

    async def asyncSetUp(self) -> None:
        # Set the LSST_DDS_PARTITION_PREFIX ENV_VAR.
        salobj.set_random_lsst_dds_partition_prefix()

        # Create the ScriptQueue Controller.
        self.controller = ScriptQueueController(index=2)

        # Start the controller and wait for it be ready.
        await self.controller.start_task

    async def test_auxtel_telescope_dome_checkout(self) -> None:
        """Execute the TelescopeDomeCheckout integration test script,
        which runs the auxtel/daytime_checkout/telescope_and_dome_checkout.py
        in ts_standardscripts.
        """
        # Instantiate the TelescopeAndDomeCheckout integration tests.
        script_class = TelescopeAndDomeCheckout()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"AuxTel Telescope and Dome Checkout; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])

    async def asyncTearDown(self) -> None:
        await self.controller.close()
        await self.controller.done_task
