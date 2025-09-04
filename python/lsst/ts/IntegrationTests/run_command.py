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

__all__ = ["RunCommand", "run_command"]

import argparse
import asyncio

import yaml
from lsst.ts.IntegrationTests import BaseScript, utils


class RunCommand(BaseScript):
    """Execute the run_command script for the given CSC and command,
    with any additional configuration parameters, placed in the
    given ScriptQueue location.

    Attributes
    ----------
    sq_index : `int`
        The index of the ScriptQueue to use to run the command.
    csc : `str`
        The <CSC>:<INDEX> for which to execute the command. Case-sensitive.
    command : `str`
        The command to execute.
    parameters : `str`
        A dictionary of parameters needed by the command, in key:value format.
    """

    configs: tuple = ()
    scripts: list = [
        ("run_command.py", BaseScript.is_standard),
    ]

    def __init__(
        self,
        sq_index: int,
        csc: str,
        command: str,
        parameters: str = "",
    ) -> None:
        super().__init__()
        self.index = sq_index
        self.csc = csc
        self.command = command
        self.parameters = parameters
        # Convert the parameters to a properly formatted dictionary.
        # First, construct the config with the CSC and Command.
        formatted_lines = [
            f"component: {self.csc}",
            f"cmd: {self.command}",
        ]
        # Second, if the command needs parameters, add them to the config.
        if self.parameters:
            formatted_lines.append("parameters:")
            # Third, construct an intermediate dictionary of the parameters.
            pairs = self.parameters.split(",")
            parameters_dict = {}
            for pair in pairs:
                key, value = pair.split(":")
                # Convert booleans regardless of capitalization.
                if value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
                else:
                    # Convert integer values.
                    try:
                        value = int(value)
                    except ValueError:
                        # Convert float values.
                        try:
                            value = float(value)
                        # Quote strings to handle spaces.
                        except ValueError:
                            value = f"'{value}'"
                parameters_dict[key] = value
            # Fourth, add the command parameters to the config.
            for key, value in parameters_dict.items():
                formatted_lines.append(f"  {key}: {value}")
        # Fifth, construct the full configuration needed for the
        # run_command.py script.
        config = "\n".join(formatted_lines)
        # Convert it to a properly formatted YAML document.
        yaml_string = yaml.safe_load(f"""{config}""")
        self.configs = (
            yaml.safe_dump(yaml_string, explicit_start=True, canonical=True),
        )


def run_command() -> None:
    # Define the script arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "sq_index",
        metavar="sq_index",
        type=int,
        choices=[1, 2, 3],
        help="Specify which ScriptQueue to use.",
    )
    parser.add_argument(
        "csc",
        metavar="csc[:index]",
        type=str,
        help="Specify which CSC[:index] to command (case sensitive).",
    )
    parser.add_argument(
        "command",
        metavar="command",
        type=str,
        help="Specify which command to execute.",
    )
    parser.add_argument(
        "-p",
        "--parameters",
        nargs="?",
        type=str,
        help="Specify any parameters for the command, in a comma-separated, key:value pair format.",
    )
    parser.add_argument(
        "-i",
        "--info",
        action="store_true",
        help="Print the allowed options.",
    )
    args = parser.parse_args()
    if args.info:
        parser.print_help()
        exit()
    # Print the help if the CSC or COMMAND is not defined.
    if not (args.csc or args.command):
        parser.print_help()
        exit()
    if args.csc.split(":")[0] not in utils.cscs:
        print(
            f"Invalid CSC: {args.csc.split(':')[0]}. "
            f"Perhaps it is misspelled or not properly capitalized."
        )
        parser.print_help()
        exit()
    main(args)


def main(opts: argparse.Namespace) -> None:
    # Ensure the invocation is correct.
    # If not, raise KeyError.
    # If it is correct, execute the command.
    try:
        script_class = RunCommand(
            sq_index=opts.sq_index,
            csc=opts.csc,
            command=opts.command,
            parameters=opts.parameters,
        )
    except KeyError as ke:
        print(repr(ke))
    else:
        print(
            f"\nExecuting the {opts.command} command "
            f"for the {opts.csc} CSC."
            f"\nRunning on ScriptQueue {opts.sq_index}."
            f"\nParameters: {script_class.parameters}."
        )
        asyncio.run(script_class.run())
