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
from lsst.ts.IntegrationTests import (
    ATPneumaticsCheckout,
    AuxTelLatissCheckout,
    AuxTelTelescopeAndDomeCheckout,
    SlewAndTakeImageCheckout,
)


class AuxTelDaytimeCheckoutTestCase(BaseTestClass):
    """Test the AuxTel Daytime Checkout integration test scripts."""

    # Use AuxTel ScriptQueue.
    index = 2

    async def test_latiss_checkout(self) -> None:
        """Execute the LatissCheckout integration test script,
        which runs the auxtel/daytime_checkout/latiss_checkout.py
        in ts_standardscripts.
        """
        # Instantiate the LatissCheckout integration tests.
        script_class = AuxTelLatissCheckout()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"LATISS Checkout; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])

    async def test_atpneumatics_checkout(self) -> None:
        """Execute the ATPneumaticsCheckout integration test script,
        which runs the auxtel/daytime_checkout/atpneumatics_checkout.py
        script in ts_auxtel_standardscripts.
        """
        # Instantiate the ATPneumaticsCheckout integration tests.
        script_class = ATPneumaticsCheckout()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"ATPneumatics  Checkout; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])

    async def test_auxtel_telescope_and_dome_checkout(self) -> None:
        """Execute the AuxTelTelescopeAndDomeCheckout integration test script,
        which runs the auxtel/daytime_checkout/telescope_and_dome_checkout.py
        in ts_standardscripts.
        """
        # Instantiate the TelescopeAndDomeCheckout integration tests.
        script_class = AuxTelTelescopeAndDomeCheckout()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"AuxTel Telescope and Dome Checkout; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])

    async def test_auxtel_slew_and_take_image_checkout(self) -> None:
        """Execute the SlewAndTakeImageCheckout integration test script,
        which runs the auxtel/daytime_checkout/telescope_and_dome_checkout.py
        in ts_standardscripts.
        """
        # Instantiate the SlewAndTakeImageCheckout integration tests.
        script_class = SlewAndTakeImageCheckout()
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(f"AuxTel Slew and Take Image Checkout; running {num_scripts} scripts")
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])
