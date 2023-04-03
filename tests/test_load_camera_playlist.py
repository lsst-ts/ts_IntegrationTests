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
import sys
import subprocess

from lsst.ts import salobj
from lsst.ts.IntegrationTests import ScriptQueueController
from lsst.ts.IntegrationTests import LoadCameraPlaylist
from lsst.ts.IntegrationTests.configs.camera_playlist_configs import (
    atcamera_playlists,
    playlist_options,
)


class LoadCameraPlaylistTestCase(unittest.IsolatedAsyncioTestCase):
    """Test the Run Camera Playlist integration test script."""

    async def asyncSetUp(self) -> None:
        # Set the LSST_DDS_PARTITION_PREFIX ENV_VAR.
        salobj.set_random_lsst_dds_partition_prefix()

        # Create the ScriptQueue Controller.
        self.controller = ScriptQueueController(index=2)

        # Start the controller and wait for it be ready.
        await self.controller.start_task

    async def test_camera_playlist(self) -> None:
        """Execute the LoadCameraPlaylist integration test script,
        which runs the ts_standardscripts/run_command.py script.
        Use the configuration stored in the camera_playlist_configs.py module.
        """
        # Mock the command-line arguments that the load_camera_playlist.py
        # script expects.
        test_camera = "at"
        test_playlist = "test"
        sys.argv[1:] = [test_camera, test_playlist]
        # Instantiate the LoadCameraPlaylist integration tests.
        script_class = LoadCameraPlaylist(
            camera=test_camera, playlist_shortname=test_playlist
        )
        # Get number of scripts
        num_scripts = len(script_class.scripts)
        # Assert the correct playlist.
        self.assertEqual(
            script_class.playlist_config["parameters"]["playlist"],
            atcamera_playlists[test_playlist],
        )
        # Assert playlist repeat is set to True.
        self.assertEqual(script_class.playlist_config["parameters"]["repeat"], True)
        print(
            f"Running the {script_class.camera} "
            f"{script_class.playlist_config['parameters']['playlist']}."
            f" Playist repeat is set to {script_class.playlist_config['parameters']['repeat']}."
        )
        # Execute the scripts.
        await script_class.run()
        # Assert script was added to correct ScriptQueue.
        self.assertEqual(len(self.controller.queue_list), num_scripts)
        self.assertEqual(script_class.index, 2)

    async def test_bad_inputs(self) -> None:
        """Attempt to execute the LoadCameraPlaylist integration test script,
        but use a bad set of command-line arguments; i.e. there is no
        playlist for the given Camera.
        """
        # Mock the command-line arguments that the load_camera_playlist.py
        # script expects.
        test_camera = "cc"
        test_playlist = "test"
        # Instantiate the LoadCameraPlaylist integration tests object and
        # execute the scripts.
        with self.assertRaises(KeyError):
            LoadCameraPlaylist(camera=test_camera, playlist_shortname=test_playlist)

    async def test_no_repeat(self) -> None:
        """Execute the LoadCameraPlaylist integration test script,
        but set playlist repeat config to False.
        """
        # Mock the command-line arguments that the load_camera_playlist.py
        # script expects.
        test_camera = "cc"
        test_playlist = "master_flat"
        test_no_repeat = False
        # Instantiate the LoadCameraPlaylist integration tests object and
        # execute the scripts.
        script_class = LoadCameraPlaylist(
            camera=test_camera, playlist_shortname=test_playlist, repeat=test_no_repeat
        )
        # Assert playlist repeat is set to False.
        self.assertEqual(script_class.playlist_config["parameters"]["repeat"], False)
        # Assert script would be added to correct ScriptQueue.
        self.assertEqual(script_class.index, 1)

    async def test_no_inputs(self) -> None:
        """Attempt to execute the LoadCameraPlaylist integration test script,
        but not use command-line arguments.  This should display the help/
        usage message.
        """
        # Execute the load_camera_playlist.py script.
        args = ["load_camera_playlist"]
        child_process = subprocess.Popen(
            args, stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        result = child_process.communicate()[0]  # type: bytes
        result_str = result.decode("utf-8")  # type: str
        print(result_str)
        if "usage" in result_str:
            assert True
        else:
            assert False

    async def test_info(self) -> None:
        """Execute the LoadCameraPlaylist integration test script,
        but use the --info flag to print out the allowed option pairs.
        """
        # Execute the load_camera_playlist.py script and capture the output.
        args = ["load_camera_playlist", "--info"]
        child_process = subprocess.Popen(
            args, stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        result = child_process.communicate()[0]  # type: bytes
        result_str = result.decode("utf-8")  # type: str
        print(result_str)
        # Assert the actual output matches the expected.
        for item in playlist_options:
            if str(item) in result_str:
                assert True
            else:
                assert False

    async def asyncTearDown(self) -> None:
        await self.controller.close()
        await self.controller.done_task
