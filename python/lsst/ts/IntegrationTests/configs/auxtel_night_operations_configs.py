# This file is part of ts_IntegrationTests.
#
# Developed for the Rubin Observatory Telescope and Site System.
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

import yaml

from .config_registry import registry


# Add the AuxTel Night Operations
# script configurations to the registry.

# auxtel_latiss_cwfs_align
registry["auxtel_cwfs_align"] = yaml.safe_dump(
    {
        "track_target": {"target_name": "HD164461"},
        "filter": "SDSSg",
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
        "reason": "IntegrationTesting",
        "program": "IntegrationTesting",
    },
    explicit_start=True,
    canonical=True,
)

# verfiy
registry["auxtel_acquire_and_take_sequence_verify"] = yaml.safe_dump(
    {
        "object_name": "HD164461",
        "acq_filter": "SDSSg",
        "acq_grating": "empty_1",
        "acq_exposure_time": 0.4,
        "target_pointing_tolerance": 6,
        "max_acq_iter": 3,
        "do_acquire": True,
        "do_take_sequence": False,
        "do_pointing_model": False,
        "target_pointing_verification": False,
        "reason": "IntegrationTesting",
        "program": "IntegrationTesting",
    },
    explicit_start=True,
    canonical=True,
)

# nominal/standard
registry["auxtel_acquire_and_take_sequence_nominal"] = yaml.safe_dump(
    {
        "object_name": "HD164461",
        "acq_filter": "SDSSg",
        "acq_grating": "empty_1",
        "grating_sequence": ["ronchi90lpmm", "ronchi90lpmm", "empty_1"],
        "filter_sequence": ["empty_1", "SDSSg", "SDSSg"],
        "exposure_time_sequence": [4.0, 4.0, 1.0],
        "target_pointing_tolerance": 5,
        "target_pointing_verification": False,
        "do_acquire": True,
        "do_take_sequence": True,
        "reason": "IntegrationTesting",
        "program": "IntegrationTesting",
    },
    explicit_start=True,
    canonical=True,
)

# test
registry["auxtel_acquire_and_take_sequence_test"] = yaml.safe_dump(
    {
        "object_name": "HD164461",
        "grating_sequence": ["ronchi90lpmm", "ronchi90lpmm", "ronchi90lpmm"],
        "filter_sequence": ["FELH0600", "SDSSg", "SDSSg"],
        "exposure_time_sequence": [5.0, 5.0, 5.0],
        "do_acquire": False,
        "do_take_sequence": True,
        "reason": "IntegrationTesting",
        "program": "IntegrationTesting",
    },
    explicit_start=True,
    canonical=True,
)
