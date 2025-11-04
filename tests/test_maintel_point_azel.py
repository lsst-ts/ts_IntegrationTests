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
from lsst.ts.IntegrationTests import MainTelPointAzEl


class MainTelPointAzElTestCase(BaseTestClass):
    """
    Test the MainTel Point AzEl integration test scripts.
    """

    # Use MainTel ScriptQueue.
    index = 1

    async def test_maintel_point_azel(self) -> None:
        """Execute the MainTelPointAzEl integration test script,
        which runs the standard/maintel/point_azel.py
        script.
        """
        # Instantiate the MainTelPointAzEl integration tests.
        args = ["0.0", "80.0", "-t", "park"]
        script_class = MainTelPointAzEl(args)
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(
            f"MainTel PointAzEl. "
            f"Running the {script_class.scripts[0][0]} script."
            f"\nAzEl coords: [{script_class.args.az},{script_class.args.el}]"
            f"\nTargetName: {script_class.args.target_name}"
            f"\nRotatorAngel: {script_class.args.rot_tel}"
            f"\nIgnore list: {script_class.args.ignore}"
        )
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])
        # Assert script arguments are correct.
        self.assertEqual(script_class.args.az, float(args[0]))
        self.assertEqual(script_class.args.el, float(args[1]))
        self.assertEqual(script_class.args.target_name, args[3])
        self.assertEqual(script_class.args.rot_tel, 0.0)
        self.assertEqual(script_class.args.ignore, [])

    async def test_maintel_point_azel_flatfield(self) -> None:
        """Execute the MainTelPointAzEl integration test script,
        which runs the standard/maintel/point_azel.py
        script.
        Test the flatfield position.
        """
        # Instantiate the MainTelPointAzEl integration tests.
        args = ["-126.2", "22.0", "-t", "flatfield", "-i", "mtdome,mtdometrajectory"]
        script_class = MainTelPointAzEl(args)
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(
            f"MainTel PointAzEl. "
            f"Running the {script_class.scripts[0][0]} script."
            f"\nAzEl coords: [{script_class.args.az},{script_class.args.el}]"
            f"\nTargetName: {script_class.args.target_name}"
            f"\nRotatorAngel: {script_class.args.rot_tel}"
            f"\nIgnore list: {script_class.args.ignore}"
        )
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])
        # Assert script arguments are correct.
        self.assertEqual(script_class.args.az, float(args[0]))
        self.assertEqual(script_class.args.el, float(args[1]))
        self.assertEqual(script_class.args.target_name, args[3])
        self.assertEqual(script_class.args.rot_tel, 0.0)
        self.assertEqual(script_class.args.ignore, [args[5]])

    async def test_maintel_point_azel_rotator_angle(self) -> None:
        """Execute the MaintelPointAzEl integration test script,
        which runs the standard/maintel/point_azel.py
        script.
        Test changing the Rotator angle using a random position.
        """
        # Instantiate the MainTelPointAzEl integration tests.
        args = ["90.0", "17.0", "-r", "45.5"]
        script_class = MainTelPointAzEl(args)
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        print(
            f"MainTel PointAzEl. "
            f"Running the {script_class.scripts[0][0]} script."
            f"\nAzEl coords: [{script_class.args.az},{script_class.args.el}]"
            f"\nTargetName: {script_class.args.target_name}"
            f"\nRotatorAngel: {script_class.args.rot_tel}"
            f"\nIgnore list: {script_class.args.ignore}"
        )
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        # Assert scripts passed.
        self.assertEqual(script_class.script_states, [8])
        # Assert script arguments are correct.
        self.assertEqual(script_class.args.az, float(args[0]))
        self.assertEqual(script_class.args.el, float(args[1]))
        self.assertEqual(script_class.args.target_name, "AzEl")
        self.assertEqual(script_class.args.rot_tel, float(args[3]))
        self.assertEqual(script_class.args.ignore, [])

    async def test_maintel_point_azel_no_args(self) -> None:
        """Execute the MainTelPointAzEl integration test script,
        which runs the standard/maintel/point_azel.py
        script.
        Leave cli arguments blank. Should fail.
        """
        # Instantiate the MainTelPointAzEl integration tests.
        with self.assertRaises(SystemExit) as e:
            MainTelPointAzEl()
        self.assertEqual(e.exception.code, 2)
