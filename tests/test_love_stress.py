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

import yaml
from lsst.ts import salobj
from lsst.ts.IntegrationTests import LoveStressTest, ScriptQueueController


class LoveStressTestCase(unittest.IsolatedAsyncioTestCase):
    """Test the LOVE Stress Test integration test script."""

    async def asyncSetUp(self) -> None:
        # Set the LSST_DDS_PARTITION_PREFIX ENV_VAR.
        salobj.set_random_lsst_dds_partition_prefix()

        # Create the ScriptQueue Controller.
        self.controller = ScriptQueueController(index=1)

        # Start the controller and wait for it be ready.
        await self.controller.start_task

    async def test_love_stress(self) -> None:
        """Execute the LoveStress integration test script,
        which runs the ts_externalscripts/make_love_stress_tests.py script.
        Use the configuration stored in the love_stress_configs.py module.

        """
        # Instantiate the LoveStress integration tests.
        script_class = LoveStressTest(test_env="bts")
        # Get number of scripts and the configuration.
        num_scripts = len(script_class.scripts)
        script_config = yaml.safe_load(script_class.configs[0])
        print(
            f"LOVE Stress Test; running {num_scripts} scripts"
            f" on the BTS environment, with this configuration: \n"
            f"{script_config}"
        )
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])
        # Assert location is correct.
        self.assertEqual(script_config["location"], "http://love01.ls.lsst.org")
        # Assert script is run in INFO mode.
        self.assertEqual(script_class.log_level, 20)

    async def test_love_stress_on_k8s(self) -> None:
        """Execute the LoveStress integration test script on the kubernetes
        LOVE instance, which runs the
        ts_externalscripts/make_love_stress_tests.py script.
        Use the configuration stored in the love_stress_configs.py module.

        """
        # Instantiate the LoveStress integration tests.
        script_class = LoveStressTest(test_env="bts", k8s="--k8s")
        # Get number of scripts and the configuration.
        num_scripts = len(script_class.scripts)
        script_config = yaml.safe_load(script_class.configs[0])
        print(
            f"LOVE Stress Test; running {num_scripts} scripts"
            f" on the BTS environment, with this configuration: \n"
            f"{script_config}"
        )
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])
        # Assert location is correct.
        self.assertEqual(script_config["location"], "https://base-lsp.lsst.codes/love")
        # Assert script is run in INFO mode.
        self.assertEqual(script_class.log_level, 20)

    async def asyncTearDown(self) -> None:
        await self.controller.close()
        await self.controller.done_task
