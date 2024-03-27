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

# Add the AuxTel Night Operations
# script configurations to the registry.

# auxtel_reset_offsets
yaml_string = yaml.safe_load(
    """
    component: "ATAOS"
    cmd: "enableCorrection"
    parameters:
      enableAll: True
    """
)
registry["auxtel_enable_all_corrections"] = yaml.safe_dump(
    yaml_string,
    explicit_start=True,
    canonical=True,
)

yaml_string = yaml.safe_load(
    """
    component: "ATAOS"
    cmd: "resetOffset"
    parameters:
      axis: "all"
    """
)
registry["auxtel_reset_offsets"] = yaml.safe_dump(
    yaml_string,
    explicit_start=True,
    canonical=True,
)

yaml_string = yaml.safe_load(
    """
    component: "ATAOS"
    cmd: "disableCorrection"
    parameters:
      disableAll: True
    """
)
registry["auxtel_disable_all_corrections"] = yaml.safe_dump(
    yaml_string,
    explicit_start=True,
    canonical=True,
)

yaml_string = yaml.safe_load(
    """
    component: "ATAOS"
    cmd: "enableCorrection"
    parameters:
      m1: True,
      hexapod: True,
      atspectrograph: True
    """
)
registry["auxtel_enable_m1_hex_atspect_corrections"] = yaml.safe_dump(
    yaml_string,
    explicit_start=True,
    canonical=True,
)

# auxtel_latiss_wep_align
registry["auxtel_wep_align"] = yaml.safe_dump(
    {
        "track_target": {"target_name": "HD164461"},
        "rot_type": "PhysicalSky",
        "filter": "SDSSr_65mm",
        "grating": "empty_1",
        "exposure_time": 5,
        "reason": "IntegrationTesting",
        "program": "IntegrationTesting",
    },
    explicit_start=True,
    canonical=True,
)

# latiss_acquire_and_take_sequence configs
# pointing
registry["auxtel_acquire_and_take_sequence_pointing"] = yaml.safe_dump(
    {
        "object_name": "HD164461",
        "acq_filter": "empty_1",
        "acq_grating": "empty_1",
        "target_pointing_tolerance": 4,
        "max_acq_iter": 4,
        "do_acquire": True,
        "do_take_sequence": False,
        "do_pointing_model": True,
        "reason": "IntegrationTesting_PointingConfiguration",
        "program": "IntegrationTesting_PointingConfiguration",
    },
    explicit_start=True,
    canonical=True,
)

# latiss_acquire and latiss_take_sequence configs
# verfiy
registry["auxtel_acquire_verify"] = yaml.safe_dump(
    {
        "object_name": "HD164461",
        "rot_type": "PhysicalSky",
        "acq_filter": "SDSSr_65mm",
        "acq_grating": "empty_1",
        "acq_exposure_time": 0.4,
        "target_pointing_tolerance": 6,
        "max_acq_iter": 3,
        "target_pointing_verification": False,
        "reason": "IntegrationTesting_VerifyConfiguration",
        "program": "IntegrationTesting_VerifyConfiguration",
    },
    explicit_start=True,
    canonical=True,
)
registry["auxtel_take_sequence_verify"] = yaml.safe_dump(
    {
        "filter_sequence": ["SDSSr_65mm"],
        "grating_sequence": ["empty_1"],
        "reason": "IntegrationTesting_VerifyConfiguration",
        "program": "IntegrationTesting_VerifyConfiguration",
    },
    explicit_start=True,
    canonical=True,
)

# nominal/standard
registry["auxtel_acquire_nominal"] = yaml.safe_dump(
    {
        "object_name": "HD164461",
        "rot_type": "PhysicalSky",
        "acq_filter": "SDSSr_65mm",
        "acq_grating": "empty_1",
        "target_pointing_tolerance": 5,
        "target_pointing_verification": False,
        "reason": "IntegrationTesting_NominalConfiguration",
        "program": "IntegrationTesting_NominalConfiguration",
    },
    explicit_start=True,
    canonical=True,
)
registry["auxtel_take_sequence_nominal"] = yaml.safe_dump(
    {
        "grating_sequence": ["holo4_003", "holo4_003", "empty_1"],
        "filter_sequence": ["empty_1", "SDSSr_65mm", "SDSSr_65mm"],
        "exposure_time_sequence": [4.0, 4.0, 1.0],
        "reason": "IntegrationTesting_NominalConfiguration",
        "program": "IntegrationTesting_NominalConfiguration",
    },
    explicit_start=True,
    canonical=True,
)

# test
registry["auxtel_acquire_test"] = yaml.safe_dump(
    {
        "object_name": "HD164461",
        "rot_type": "PhysicalSky",
        "reason": "IntegrationTesting_TestConfiguration",
        "program": "IntegrationTesting_TestConfiguration",
    },
    explicit_start=True,
    canonical=True,
)
registry["auxtel_take_sequence_test"] = yaml.safe_dump(
    {
        "grating_sequence": ["holo4_003", "holo4_003", "holo4_003"],
        "filter_sequence": ["SDSSr_65mm", "SDSSr_65mm", "SDSSr_65mm"],
        "exposure_time_sequence": [5.0, 5.0, 5.0],
        "reason": "IntegrationTesting_TestConfiguration",
        "program": "IntegrationTesting_TestConfiguration",
    },
    explicit_start=True,
    canonical=True,
)
