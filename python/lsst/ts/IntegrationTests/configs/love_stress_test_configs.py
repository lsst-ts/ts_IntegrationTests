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

# Add the LOVE Stress Test script
# configurations to the registry.

registry["love_stress"] = yaml.safe_dump(
    {
        "location": "love1.tu.lsst.org",
        "number_of_clients": 50,
        "number_of_messages": 5000,
        "data": [
            "ATAOS:0",
            "ATCamera:0",
            "ATDome:0",
            "ATDomeTrajectory:0",
            "ATMCS:0",
            "ATHexapod:0",
            "ATPneumatics:0",
            "ATPtg:0",
            "ATSpectrograph:0",
            "ESS:301",
            "LaserTracker:1",
            "MTAirCompressor:1",
            "MTAirCompressor:2",
            "MTMount:0",
            "MTPtg:0",
            "MTDome:0",
            "MTDomeTrajectory:0",
            "MTAOS:0",
            "MTHexapod:1",
            "MTHexapod:2",
            "MTRotator:0",
            "MTM1M3:0",
            "MTM2:0",
            "Scheduler:1",
            "Scheduler:2",
            "Watcher:0",
        ],
    },
    explicit_start=True,
    canonical=True,
)
