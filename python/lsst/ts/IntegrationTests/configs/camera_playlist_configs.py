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

import yaml

from .config_registry import registry

# Create the list Camera short-names.

cameras = ["at", "cc"]

# Create the Camera short-name to playlist dictionary.

atcamera_playlists = {
    "master_flat": "bias_dark_flat",
    "master_ptc": "bias_dark_ptc",
    "cwfs": "cwfs-test_take_sequence",
    "nominal": "latiss_acquire_and_take_sequence-test_take_acquisition_nominal",
    "pointing": "latiss_acquire_and_take_sequence-test_take_acquisition_pointing",
    "verify": "latiss_acquire_and_take_sequence-test_take_acquisition_with_verification",
    "test": "latiss_acquire_and_take_sequence-test_take_sequence",
}

cccamera_playlists = {
    "master_flat": "bias_dark_flat",
    "master_ptc": "bias_dark_ptc",
}

# Define the sorted list of unique playlist short-names.

playlists = sorted(
    list(set(list(cccamera_playlists.keys()) + list(atcamera_playlists.keys())))
)

# Create the sorted list of allowable Camera-PlaylistShortname options.

playlist_options = []
for item in list(cccamera_playlists.keys()):
    playlist_options.append(("cc", item))
for item in list(atcamera_playlists.keys()):
    playlist_options.append(("at", item))
playlist_options.sort()

# Add the script configurations to the configuration registry.

yaml_string = yaml.safe_load(
    """
    component: "replace_me"
    cmd: "play"
    parameters:
        playlist: "replace_me"
        repeat: True
    """
)

registry["camera_playlist"] = yaml.safe_dump(
    yaml_string,
    explicit_start=True,
    canonical=True,
)
