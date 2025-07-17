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
from datetime import date

from lsst.ts import salobj
from lsst.ts.IntegrationTests import LsstCamCalibrations, ScriptQueueController


class LsstCamCalibrationsTestCase(unittest.IsolatedAsyncioTestCase):
    """
    Test the Make Latiss Configurations integration test scripts.
    """

    async def asyncSetUp(self) -> None:
        # Define LSST_TOPIC_SUBNAME.
        salobj.set_test_topic_subname()

        # Create the ScriptQueue Controller.
        self.controller = ScriptQueueController(index=1)

        # Start the controller and wait for it be ready.
        await self.controller.start_task

    async def test_lsstcam_calibrations_flat(self) -> None:
        """Execute the LsstCamCalibrations integration test script,
        which runs the ts_standardscripts/maintel/make_lsstcam_calibratons.py
        script.
        Use the configuration stored in the image_taking_configs.py module.
        """
        # Instantiate the LsstCamCalibrations integration tests.
        calib_type = "flat"
        script_class = LsstCamCalibrations(calib_type=calib_type)
        # Assert configurations were updated with current date.
        self.assertEqual(
            script_class.calib_configs["certify_calib_begin_date"],
            date.today().strftime("%Y-%m-%d"),
        )
        self.assertEqual(
            script_class.calib_configs["calib_collection"],
            f"LSSTCam/calib/u/integrationtester/daily."
            f"{date.today().strftime('%Y%m%d')}.{calib_type}",
        )
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(
            f"AuxTel Make Latiss Configurations. "
            f"Running the {script_class.scripts[0][0]} script "
            f"for the master_{calib_type} calibrations,"
            f"\nwith configuration;\n{script_class.configs}"
        )
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])
