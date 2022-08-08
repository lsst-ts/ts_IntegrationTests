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
from lsst.ts.IntegrationTests import ComCamImageTaking


class RunImageTakingVerificationTestCase(unittest.IsolatedAsyncioTestCase):
    """
    Test the Run Camera Image Taking Verficicattion integration test scripts.
    """

    async def asyncSetUp(self) -> None:
        # Set the LSST_DDS_PARTITION_PREFIX ENV_VAR.
        salobj.set_random_lsst_dds_partition_prefix()

        # Create the ScriptQueue Controller.
        self.controller = ScriptQueueController(index=1)

        # Start the controller and wait for it be ready.
        await self.controller.start_task

    async def test_comcam_image_taking(self) -> None:
        """Execute the ComCamImageTaking integration test script,
        which runs the ts_standardscripts/take_image_comcam.py script.
        Use the configuration stored in the image_taking_configs.py module.
        """
        # Instantiate the ComCamImageTaking integration tests object and
        # execute the scripts.
        script_class = ComCamImageTaking()
        await script_class.run()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(
            f"ComCam Image Taking verification. "
            f"Running the {script_class.scripts[0][0]} script."
        )
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
