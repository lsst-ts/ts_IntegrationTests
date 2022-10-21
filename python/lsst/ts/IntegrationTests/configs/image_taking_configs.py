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


# Add the AuxTel and ComCam image taking verification
# script configurations to the registry.

# auxtel_image_taking
registry["image_taking"] = yaml.safe_dump(
    {
        "nimages": 1,
        "image_type": "BIAS",
        "program": "IntegrationTesting",
        "reason": "SystemCheckout",
    },
    explicit_start=True,
    canonical=True,
)

# auxtel_latiss_calibrations
registry["latiss_calibrations_flat"] = yaml.safe_dump(
    {
        "n_bias": 10,
        "n_dark": 10,
        "exp_times_dark": 10,
        "n_flat": 10,
        "exp_times_flat": 2,
        "filter": "SDSSr",
        "calib_collection": "LATISS/calib/u/integrationtester/daily.replace_me.calib_type",
        "generate_calibrations": True,
        "do_verify": True,
        "script_mode": "BIAS_DARK_FLAT",
        "do_defects": True,
        "certify_calib_begin_date": "replace_me",
    },
    explicit_start=True,
    canonical=True,
)

registry["latiss_calibrations_ptc"] = yaml.safe_dump(
    {
        "n_bias": 10,
        "n_dark": 10,
        "exp_times_dark": 10,
        "n_flat": 40,
        "filter": "BG40",
        "exp_times_flat": [
            0.2,
            0.2,
            0.4,
            0.4,
            0.6,
            0.6,
            0.8,
            0.8,
            1.0,
            1.0,
            1.2,
            1.2,
            1.4,
            1.4,
            1.6,
            1.6,
            1.8,
            1.8,
            2.0,
            2.0,
            2.2,
            2.2,
            2.4,
            2.4,
            2.6,
            2.6,
            2.8,
            2.8,
            3.0,
            3.0,
            3.2,
            3.2,
            3.4,
            3.4,
            3.6,
            3.6,
            3.8,
            3.8,
            4.0,
            4.0,
        ],
        "calib_collection": "LATISS/calib/u/integrationtester/daily.replace_me.calib_type",
        "generate_calibrations": True,
        "do_verify": True,
        "script_mode": "BIAS_DARK_FLAT",
        "do_defects": True,
        "do_ptc": True,
        "certify_calib_begin_date": "replace_me",
    },
    explicit_start=True,
    canonical=True,
)

# comcam_calibrations
registry["comcam_calibrations_flat"] = yaml.safe_dump(
    {
        "n_bias": 10,
        "n_dark": 10,
        "exp_times_dark": 20,
        "n_flat": 10,
        "exp_times_flat": 5,
        "detectors": [0, 1, 2, 3, 4, 5, 6, 7, 8],
        "filter": "r_03",
        "calib_collection": "LSSTComCam/calib/u/integrationtester/daily.replace_me.calib_type",
        "generate_calibrations": True,
        "do_verify": True,
        "script_mode": "BIAS_DARK_FLAT",
        "do_defects": True,
        "certify_calib_begin_date": "replace_me",
    },
    explicit_start=True,
    canonical=True,
)
