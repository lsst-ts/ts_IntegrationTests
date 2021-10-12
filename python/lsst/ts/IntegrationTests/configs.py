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


class AuxTelVisitConfig:
    """Defines the configuration used in the AuxTel Visit
    integration test script.

    """

    def __init__(self, nimages, exp_time, image_type, cam_filter, grating):
        self.nimages = nimages
        self.exp_time = exp_time
        self.image_type = image_type
        self.cam_filter = cam_filter
        self.grating = grating

    def __new__(cls, nimages, exp_time, image_type, cam_filter, grating):
        config = yaml.safe_dump(
            {
                "nimages": nimages,
                "exp_times": exp_time,
                "image_type": image_type,
                "filter": cam_filter,
                "grating": grating,
                "linear_stage": None,
            },
            explicit_start=True,
            canonical=True,
        )
        return config


auxtel_visit_config1 = AuxTelVisitConfig(1.0, 5.0, "OBJECT", "FELH0600", "ronchi90lpmm")
auxtel_visit_config2 = AuxTelVisitConfig(1.0, 5.0, "OBJECT", "BG40", "ronchi90lpmm")
auxtel_visit_config3 = AuxTelVisitConfig(1.0, 5.0, "OBJECT", "BG40", "holo4_003")
auxtel_visit_config4 = AuxTelVisitConfig(1.0, 5.0, "OBJECT", "FELH0600", "holo4_003")
auxtel_visit_config5 = AuxTelVisitConfig(1.0, 5.0, "OBJECT", "FELH0600", "empty_1")
auxtel_visit_config6 = AuxTelVisitConfig(1.0, 5.0, "OBJECT", "BG40", "empty_1")
