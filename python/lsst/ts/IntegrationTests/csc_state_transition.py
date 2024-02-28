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

__all__ = ["CSCStateTransition", "csc_state_transition"]

import argparse
import asyncio

import yaml
from lsst.ts.IntegrationTests import BaseScript, utils


class CSCStateTransition(BaseScript):
    """Execute the set_summary_state script for the given CSC,
    with any additional configuration parameters,
    placed in the given ScriptQueue location.

    Attributes
    ----------
    csc : `str`
        The name of the CSC to transition. Case-sensitive.
    csc_index : `int`
        The index value for the indexed-CSC.
    state : `str`
        The state to transition.
    additional_configuration : `str`
        Any additional state-transition configuration items.
    """

    configs: tuple = ()
    scripts: list = [
        ("set_summary_state.py", BaseScript.is_standard),
    ]

    def __init__(
        self,
        csc: str,
        state: str,
        csc_index: int = 0,
        additional_configuration: str = "",
    ) -> None:
        super().__init__()
        self.csc = csc
        self.csc_index = csc_index
        self.state = state
        self.added_config = additional_configuration
        # Set the ScriptQueue index based on which telescope.
        if csc[:2].lower() == "at":
            self.index = 2
        else:
            self.index = 1
        # Construct the intermediate configuration list.
        # Convert the list to a string.
        if self.csc_index:
            full_csc_name = f"{self.csc}:{self.csc_index}"
        else:
            full_csc_name = self.csc
        temp_config = [full_csc_name, self.state]
        if self.added_config:
            temp_config.append(self.added_config)
        config = ", ".join(str(i) for i in temp_config)
        # Construct the full configuration needed for the
        # set_summary_state.py script.
        # Convert it to a properly formatted YAML document.
        yaml_string = yaml.safe_load(
            f"""
            data:
            - [{config}]
            """
        )
        self.configs = (
            yaml.safe_dump(yaml_string, explicit_start=True, canonical=True),
        )


def csc_state_transition() -> None:
    # Define the lists of CSC and State options.
    csc_list = list(utils.cscs)
    csc_list.sort()
    state_list = list(utils.csc_states)
    state_list.sort()
    # Define the script arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "csc",
        metavar="csc",
        nargs="?",
        type=str,
        choices=csc_list,
        help="Specify which CSC to command (case sensitive).",
    )
    parser.add_argument(
        "state",
        metavar="state",
        nargs="?",
        type=str,
        choices=state_list,
        help="Specify to which state to transition.",
    )
    parser.add_argument(
        "-x",
        "--csc_index",
        metavar="index",
        nargs="?",
        type=int,
        help="Define the index of the CSC, if applicable.",
    )
    parser.add_argument(
        "-a",
        "--additional_configuration",
        nargs="?",
        type=str,
        help="Specify any additional configurations.",
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
    if not (args.info or args.csc or args.state):
        parser.print_help()
        exit()
    if args.info:
        print(
            f"\nThe allowed options are:\n"
            f"  csc:\t{csc_list}\n\n"
            f"  state:\t{state_list}\n"
        )
        exit()
    if args.csc not in utils.cscs:
        print(
            f"Invalid CSC: {args.csc}. "
            f"Perhaps it is misspelled or not properly capitalized."
        )
        parser.print_help()
        exit()
    main(args)


def main(opts: argparse.Namespace) -> None:
    # Ensure the invocation is correct.
    # If not, raise KeyError.
    # If it is correct, execute the state transition.
    try:
        script_class = CSCStateTransition(
            csc=opts.csc,
            state=opts.state,
            additional_configuration=opts.additional_configuration,
        )
    except KeyError as ke:
        print(repr(ke))
    else:
        print(
            f"\nTransitioning the {opts.csc.upper()} "
            f"to the {opts.state} state."
            f"\nConfiguration: {script_class.configs}."
        )
        asyncio.run(script_class.run())
