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

__all__ = ["BaseScript"]

import asyncio
import copy
from datetime import date

from lsst.ts import salobj
from lsst.ts.idl.enums.Script import ScriptState
from lsst.ts.idl.enums.ScriptQueue import Location, ScriptProcessState

import utils.py


class BaseScript:
    """Defines the common attributes and functions for an
       AuxTel or MainTel script.

    Notes
    -----
    Use index=1 for MainTel, 2 for AuxTel. The index is defined as a class
    attribute for simplicity.  The sub-Classes define which index,
    if necessary.
    The BaseScript class defaults to index=1, as the most common option.

    Attributes
    ----------
    index : `int`
        The index represents the Main Telescope, index=1, or the
        Auxilliary Telescope, index=2.
    is_standard : boolean
        Variable used to specify the script as Standard; value is True.
        Used for readability.
    is_external : boolean
        Variable used to specify the script as External; value is False.
        Used for readability.
    configs : `tuple`
        The list of Yaml-formatted script configurations.
        They are stored in the configs.py module.
    scripts : `list`
        A list of tuples. The tuple is the script name and a boolean.
        The boolean specifies the script as Standard (True)
        or External (False).
    """

    # See Attributes for the definition.
    index: int = 1
    is_standard: bool = True
    is_external: bool = False
    configs: tuple = ()
    scripts: list = []

    def __init__(self, queue_placement: str = "LAST") -> None:
        """Initialize the given Standard or External
           script, with the given Yaml configuration, placed in the
           given ScriptQueue location.

        Parameters
        ----------
        remote : `salobj.Remote`
            A listener for the ScriptQueue CSC. Defined as an instance
            variable, in order to call it from mulitple methods.
        queue_placement : `str`
            Options are "FIRST" "LAST" "BEFORE" or "AFTER" and are
            case insensistive ("FIRST" is the default, for convenience).
            The BaseScript Class will convert to the appropriate
            ScriptQueue.Location enum object.
        script_states : `list`
            The list of script states as integers. This list is used by
            both the run() and wait_for_done() functions, so must be
            defined as an instance variable.
        temp_script_indexes : `list`
            A temporary copy of the script_indexes list. This list is reduced
            by the wait_for_done() function until all the scripts are complete.
            This maintains the integrity of the real script_indexes list.
        all_scripts_done : `bool`
            A simple boolean variable, defaulting to False, that is set to
            True once all the scripts are complete.
        """
        self.remote: salobj.Remote
        self.queue_placement: str = queue_placement
        self.script_states: list[int] = []
        self.temp_script_indexes: list[int] = []
        self.all_scripts_done: bool = False

    @classmethod
    def get_current_date(cls, date_format: str = "%Y-%m-%d") -> str:
        """Returns the current date, in the given format.
           This is used in the Calibration tests, to assign the storage
           directory.

        Parameters
        ----------
        format : `str`
            The format for the date string. Default is "%Y-%m-%d."
        """
        return date.today().strftime(date_format)

    @classmethod
    def add_arguments(cls, **kwargs: str) -> None:
        """Add additional command line arguments to the script constructor.

        Parameters
        ----------
        **kwargs : `dict`, optional
            Additional keyword arguments for your script's constructor.
        Returns
        -------
        """
        pass

    async def wait_for_done(self, data: salobj.BaseMsgType) -> None:
        """Wait for the scripts to be in one of defined terminal states.

        Parameters
        ----------
        data : ``lsst.ts.salobj.BaseMsgType``
            The object returned by the ScriptQueue Script Event (evt_script).
        """
        if data.processState in utils.processing_states:
            # Script initial, configuration and running states.
            print(
                f"Script processing state: "
                f"{ScriptProcessState(data.processState).name}"
            )
            return
        print(f"Waiting for script ID {self.temp_script_indexes[0]} to finish...")
        if data.processState in utils.terminal_states and data.timestampProcessEnd > 0:
            print(
                f"Script {data.scriptSalIndex} terminal processing state: "
                f"{ScriptProcessState(data.processState).name}\n"
                f"Final ScriptState: {ScriptState(data.scriptState).name}"
            )
            # Store the final Script.ScriptState enum
            # in the script_states list.
            self.script_states.append(int(data.scriptState))
            # Scripts run sequentially and FIFO.
            # When done, remove the leading script.
            self.temp_script_indexes.pop(0)
            # Set the all_scripts_done flag to True when all the
            # scripts are complete.
            self.all_scripts_done = len(self.temp_script_indexes) == 0
            # Resume the ScriptQueue, if a script failed,
            # to continue processing any remaining scripts.
            # NOTE: This MUST be done LAST. Otherwise, the resume triggers an
            # additional set of callbacks, but the self.temp_script_indexes
            # list is empty and the .pop(0) method fails with an IndexError.
            if data.scriptState == ScriptState.FAILED:
                print("Resuming the ScriptQueue after a script FAILED.")
                await self.remote.cmd_resume.set_start(timeout=10)

    async def run(self) -> None:
        """Run the specified standard or external scripts.
        Wait for the scripts to finish and print the lists of
        script indexes and script states.
        """
        async with salobj.Domain() as domain, salobj.Remote(
            domain=domain, name="ScriptQueue", index=self.index
        ) as self.remote:
            # Since `async with` is used,
            # you do NOT have to wait for the remote to start

            # Create the callback to the ScriptQueue Script Event that
            # will wait for all the scripts to complete.
            self.remote.evt_script.callback = self.wait_for_done
            # Convert the queue_placement parameter to the approprirate
            # ScriptQueue.Location Enum object.
            queue_placement = getattr(Location, self.queue_placement.upper())

            # Wait for the next ScriptQueue heartbeat to ensure it is running.
            await self.remote.evt_heartbeat.next(flush=True, timeout=30)
            # Pause the ScriptQueue to load the scripts into the queue.
            await self.remote.cmd_pause.start(timeout=10)
            # Add scripts to the queue.
            script_indexes = []
            for script, config in zip(self.scripts, self.configs):
                ack = await self.remote.cmd_add.set_start(
                    timeout=10,
                    isStandard=script[1],
                    path=script[0],
                    config=config,
                    logLevel=10,
                    location=queue_placement,
                )
                try:
                    script_indexes.append(int(ack.result))
                except Exception:
                    print(f"Something went wrong: {ack.result}")
            # Copy the script_indexes list to use in the Script Event callback.
            # This maintains the integrity of the real script_indexes list.
            self.temp_script_indexes = copy.deepcopy(script_indexes)
            # Resume the ScriptQueue to begin script execution.
            await self.remote.cmd_resume.set_start(timeout=10)
            # Wait for the scripts to complete.
            while not self.all_scripts_done:
                await asyncio.sleep(0)
            # Print the script indexes and states.
            print(
                f"All scripts complete.\n"
                f"Script Indexes ; Script States:\n"
                f"{script_indexes}\n{self.script_states}"
            )
