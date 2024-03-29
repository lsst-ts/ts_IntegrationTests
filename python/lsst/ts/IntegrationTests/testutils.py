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

import subprocess


def assert_yaml_formatted(reference: str, yaml_string: str) -> None:
    """Assert that the given string is properly yaml formatted.

    To call this from a unit test (see ``tests/test_yaml.py``)::

        IntegrationTests.assert_yaml_formatted(yaml_string)

    Parameters
    ----------
    referernce : `str`
        String used to reference or identify the yaml_string.
    yaml_string : `str`
        String, either stdin or printed content from a file.

    Raises
    ------
    AssertionError
        If string not formatted properly as assessed by ``yamllint``.

    Notes
    -----
    Yamllint works with files or stdin, but the invocation syntax is
    different. Most instances in the integration testing will be
    strings, so this test uses the stdin invocation.
    """
    args = ["yamllint", "-"]
    byte_string = bytes(yaml_string, "utf-8")
    child_proccess = subprocess.Popen(
        args, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    child_proccess.stdin.write(byte_string)  # type: ignore
    result = child_proccess.communicate()[0]  # type: bytes
    result_str = result.decode("utf-8")  # type: str
    child_proccess.stdin.close()  # type: ignore
    if any(exception in result_str for exception in ("warning", "error")):
        raise AssertionError(
            f"Bad YAML\n\n{reference!r}:\n'{yaml_string!r}'\n\n{result!r}"
        )  # type: ignore


def logging_statement(statement: str) -> None:
    """Print a logging statement

    Parameters
    ----------
    statement : `string`
        statement; The string to print
    """
    print(statement)
