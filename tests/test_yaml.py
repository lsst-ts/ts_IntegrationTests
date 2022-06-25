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

import unittest
import subprocess

from lsst.ts import IntegrationTests
from lsst.ts.IntegrationTests.configs.config_registry import registry


class YamlTestCase(unittest.TestCase):
    """Test that the configurations are stored as properly formatted
    Yaml strings.

    """

    def test_yaml_formatted(self) -> None:
        """Use the IntegrationTests.yaml_test_string1() configuration to test
        a well-formatted Yaml string.

        """
        yaml_string = IntegrationTests.yaml_test_string1()
        IntegrationTests.assert_yaml_formatted("test", yaml_string)

    def test_bad_yaml(self) -> None:
        """Use the IntegrationTests.bad_yaml() configuration to test
        a non-Yaml-formatted string.

        """
        bad_yaml = IntegrationTests.bad_yaml()
        args = ["yamllint", "-"]
        byte_string = bytes(bad_yaml, "utf-8")
        child_proccess = subprocess.Popen(
            args, stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        child_proccess.stdin.write(byte_string)  # type: ignore
        result = child_proccess.communicate()[0]  # type: bytes
        result_str = result.decode("utf-8")  # type: str
        child_proccess.stdin.close()  # type: ignore
        if any(exception in result_str for exception in ("warning", "error")):
            assert True
        else:
            assert False

    def test_script_configs(self) -> None:
        """Test the IntegrationTests.configs are
        well-formatted Yaml.

        """
        # Get the keys from the configuration registry (dict).
        registry_keys = list(registry.keys())
        # Ensure the registry contains the configurations.
        length = len(registry_keys)
        assert length > 0
        # Verify the configurations are properly YAML-formatted.
        for key in registry_keys:
            yaml_string = registry[key]
            IntegrationTests.assert_yaml_formatted(key, yaml_string)
