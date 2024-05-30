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

import argparse

from lsst.ts.idl.enums.ScriptQueue import ScriptProcessState

# Define the various lists used by the modules in this package.

# Define the list of CSCs.
# This is needed to validate the csc_state_transition configuration.
cscs = frozenset(
    [
        "ATAOS",
        "MTAirCompressor",
        "ATBuilding",
        "ATCamera",
        "ATDome",
        "ATDomeTrajectory",
        "ATHeaderService",
        "ATHexapod",
        "ATMCS",
        "ATMonochromator",
        "ATOODS",
        "ATPneumatics",
        "ATPtg",
        "ATSpectrograph",
        "ATWhiteLight",
        "Authorize",
        "GCHeaderService",
        "CCCamera",
        "CCHeaderService",
        "CCOODS",
        "CBP",
        "DIMM",
        "DREAM",
        "DSM",
        "EAS",
        "Electrometer",
        "EPM",
        "ESS",
        "FiberSpectrograph",
        "GenericCamera",
        "GIS",
        "Guider",
        "HVAC",
        "LaserTracker",
        "LEDProjector",
        "LinearStage",
        "LOVE",
        "MTAOS",
        "MTCamera",
        "MTDome",
        "MTDomeTrajectory",
        "MTEEC",
        "MTHeaderService",
        "MTHexapod",
        "MTM1M3",
        "MTM1M3TS",
        "MTM2",
        "MTMount",
        "MTOODS",
        "MTPtg",
        "MTRotator",
        "MTVMS",
        "OCPS:2",
        "OCPS:3",
        "PMD",
        "Scheduler",
        "Script",
        "ScriptQueue",
        "SummitFacility",
        "Test",
        "TunableLaser",
        "Watcher",
        "WeatherForecast",
    ]
)

# Define the list of CSC States.
csc_states = frozenset(
    [
        "Offline",
        "Standby",
        "Disabled",
        "Enabled",
    ]
)

# Define the set of script states that indicate the script is processing.
processing_states = frozenset(
    (
        ScriptProcessState.UNKNOWN,
        ScriptProcessState.LOADING,
        ScriptProcessState.CONFIGURED,
        ScriptProcessState.RUNNING,
    )
)

# Define the set of script states that indicate the script is complete.
terminal_states = frozenset(
    (
        ScriptProcessState.DONE,
        ScriptProcessState.LOADFAILED,
        ScriptProcessState.CONFIGURE_FAILED,
        ScriptProcessState.TERMINATED,
    )
)


def get_test_env_arg() -> argparse.Namespace:
    # Define the script arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "test_env",
        nargs="?",
        type=str.lower,
        choices=["bts", "tts", "summit"],
        help="Specify on which environment the tests are running (case insensitive).",
    )
    parser.add_argument(
        "--k8s",
        default=False,
        action="store_true",
        help="Specify if the tests are running against the kubernetes instance.",
    )
    args = parser.parse_args()
    # Print the help if the environment is not defined.
    if not (args.test_env):
        parser.print_help()
        exit()
    return args
