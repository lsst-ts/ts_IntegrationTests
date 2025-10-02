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
    sq_index : `int`
        The index of the ScriptQueue to use to run the state transition.
    additional_configuration : `str`
        Any additional state-transition configuration items.
    mute_alarms : `bool`
        The set_summary_state accepts a boolean argument to command the Watcher
        to mute alarms. This is necessary when moving a CSC to Offline.
    """

    configs: tuple = ()
    scripts: list = [
        ("set_summary_state.py", BaseScript.is_standard),
    ]

    def __init__(
        self,
        csc: str,
        state: str,
        sq_index: int,
        additional_configuration: str = "",
        mute_alarms: bool = False,
    ) -> None:
        super().__init__()
        self.csc = csc
        self.state = state
        self.index = sq_index
        self.added_config = additional_configuration
        self.mute_alarms = mute_alarms
        # Construct the intermediate configuration list.
        # Convert the list to a string.
        temp_config = [self.csc, self.state]
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
            mute_alarms: self.mute_alarms
            """
        )
        self.configs = (
            yaml.safe_dump(yaml_string, explicit_start=True, canonical=True),
        )


def csc_state_transition() -> None:
    # Define the State options lists.
    state_list = list(utils.csc_states)
    state_list.sort()
    # Define the script arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "csc",
        metavar="csc[:index]",
        type=str,
        help="Specify which CSC[:index] to command (case sensitive).",
    )
    parser.add_argument(
        "state",
        metavar="state",
        type=str,
        choices=state_list,
        help="Specify to which state to transition.",
    )
    parser.add_argument(
        "sq_index",
        metavar="scriptqueue_index",
        type=int,
        choices=[1, 2, 3],
        help="Specify which ScriptQueue to use.",
    )
    parser.add_argument(
        "-a",
        "--additional_configuration",
        nargs="?",
        type=str,
        help="Specify any additional configurations.",
    )
    parser.add_argument(
        "-m",
        "--mute_alarms",
        type=bool,
        action="store_true",
        help="Tell the Watcher to mute alarms. Include if setting CSC to Offline.",
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
    # Print the help if the CSC or STATE is not defined.
    if not (args.csc or args.state):
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
    # If it is correct, execute the state transition.
    try:
        script_class = CSCStateTransition(
            csc=opts.csc,
            state=opts.state,
            sq_index=opts.sq_index,
            additional_configuration=opts.additional_configuration,
        )
    except KeyError as ke:
        print(repr(ke))
    else:
        print(
            f"\nTransitioning the {opts.csc.upper()} "
            f"to the {opts.state} state."
            f"\nRunning on ScriptQueue {opts.sq_index}."
            f"\nConfiguration: {script_class.configs}."
            f"\nMute Alarms: {script_class.mute_alarms}."
        )
        asyncio.run(script_class.run())
