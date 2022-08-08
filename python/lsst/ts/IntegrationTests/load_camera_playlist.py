# This file is part of ts_IntegrationTests
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

__all__ = ["LoadCameraPlaylist", "load_camera_playlist"]

import yaml
import os
import argparse
import asyncio

import lsst.ts.IntegrationTests.configs.camera_playlist_configs as playlist_configs
from lsst.ts.IntegrationTests import BaseScript
from lsst.ts.IntegrationTests.configs.config_registry import registry
from lsst.ts.IntegrationTests.configs.camera_playlist_configs import (
    cameras,
    playlists,
    playlist_options,
)


class LoadCameraPlaylist(BaseScript):
    """Execute the run_command script for the given Playlist,
    for the given Camera, with the given Yaml configuration,
    placed in the given ScriptQueue location.

    """

    index: int = 2
    configs: tuple = ()
    scripts: list = [
        ("run_command.py", BaseScript.is_standard),
    ]

    def __init__(
        self, camera: str, playlist_shortname: str, repeat: bool = True
    ) -> None:
        super().__init__()
        self.camera = camera
        self.camera_full = camera.upper() + "Camera"
        playlist_dictionary = getattr(
            playlist_configs, self.camera + "camera_playlists"
        )
        try:
            self.playlist = playlist_dictionary[playlist_shortname]
        except KeyError:
            raise KeyError(
                f"The {self.camera_full} does not have a '{playlist_shortname}' playlist."
            )
        self.playlist_config = yaml.safe_load(registry["camera_playlist"])
        self.playlist_config["component"] = self.camera_full
        self.playlist_config["parameters"]["playlist"] = self.playlist
        self.playlist_config["parameters"]["repeat"] = repeat
        self.configs = (yaml.safe_dump(self.playlist_config),)


def load_camera_playlist() -> None:
    # Define the script arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "camera",
        metavar="camera",
        nargs="?",
        type=str.lower,
        choices=cameras,
        help="Specify which Camera to command (case insensitive).",
    )
    parser.add_argument(
        "playlist_shortname",
        metavar="playlist_shortname",
        nargs="?",
        type=str.lower,
        choices=playlists,
        help="Specify the playlist short name.",
    )
    parser.add_argument(
        "--no-repeat",
        action="store_true",
        help="Disable playlist repeat.",
    )
    parser.add_argument(
        "-i",
        "--info",
        action="store_true",
        help="Print the allowed options.",
    )
    args = parser.parse_args()
    # Print the help if the camera is not defined,
    # or info is not passed.
    if not (args.info or args.camera):
        parser.print_help()
        exit()
    # Print the playlist options when the info flag is passed.
    if args.info:
        print("The allowed options are: ")
        print(*playlist_options, sep=os.linesep)
        exit()
    main(args)


def main(opts: argparse.Namespace) -> None:
    # Set the playlist repeat config value
    repeat = True
    if opts.no_repeat:
        repeat = False
    # Ensure the invocation is correct.
    # If not, raise KeyError.
    # If it is correct, execute the camera playlist.
    try:
        script_class = LoadCameraPlaylist(
            camera=opts.camera,
            playlist_shortname=opts.playlist_shortname,
            repeat=repeat,
        )
    except KeyError as ke:
        print(repr(ke))
    else:
        print(
            f"\nExecuting the {opts.camera.upper()}Camera "
            f"'{opts.playlist_shortname}' playlist."
            f" Playlist repeat is {repeat}."
        )
        asyncio.run(script_class.run())
