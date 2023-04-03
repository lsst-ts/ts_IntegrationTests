# This file is part of ts_IntegrationTests
#
# Developed for the LSST Telescope and Site Systems.
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

__all__ = ["BaseScript"]

from lsst.ts import salobj
from lsst.ts.idl.enums import ScriptQueue
from lsst.ts.idl.enums.Script import ScriptState

from datetime import date


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

    # Define the set of script states that indicate the script is complete.
    terminal_states = frozenset(
        (
            ScriptState.DONE,
            ScriptState.STOPPED,
            ScriptState.FAILED,
            ScriptState.CONFIGURE_FAILED,
        )
    )

    def __init__(self, queue_placement: str = "LAST") -> None:
        """Initialize the given Standard or External
           script, with the given Yaml configuration, placed in the
           given ScriptQueue location.

        Parameters
        ----------
        queue_placement : `str`
            Options are "FIRST" "LAST" "BEFORE" or "AFTER" and are
            case insensistive ("FIRST" is the default, for convenience).
            The BaseScript Class will convert to the appropriate
            ScriptQueue.Location enum object.

        """
        self.queue_placement = queue_placement

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

    async def wait_for_script_done(
        self, scriptqueue_remote: salobj.Remote, sal_index: int, timeout: int = 900
    ) -> int:
        """Wait for a script to finish and return the final state.

        Warning: this ignores messages for all other scripts.

        Parameters
        ----------
        scriptqueue_remote : `salobj.Remote`
            The ScriptQueue Remote object from SalObj.
        sal_index : `int`
            The SAL index value of the script.
        timeout : `float`
            How long to wait for the script to complete. Default is 900s.

        Returns
        -------
        scriptState : `int`
            The state of the script.
        """
        while True:
            data = await scriptqueue_remote.evt_script.next(
                flush=False, timeout=timeout
            )
            if data.scriptSalIndex != sal_index:
                continue
            if data.scriptState in self.terminal_states:
                return data.scriptState

    async def run(self) -> None:
        """Run the specified standard or external scripts.
        Wait for the scripts to finish and print the lists of
        script indexes and script states.
        """
        async with salobj.Domain() as domain, salobj.Remote(
            domain=domain, name="ScriptQueue", index=self.index
        ) as remote:
            # Since `async with` is used,
            # you do NOT have to wait for the remote to start

            # Convert the queue_placement parameter to the approprirate
            # ScriptQueue.Location Enum object.
            queue_placement = getattr(
                ScriptQueue.Location, self.queue_placement.upper()
            )

            # Wait for the next ScriptQueue heartbeat to ensure it is running.
            await remote.evt_heartbeat.next(flush=True, timeout=30)
            # Pause the ScriptQueue to load the scripts into the queue.
            await remote.cmd_pause.start(timeout=10)
            # Add scripts to the queue.
            script_indexes = []
            script_states = []
            for script, config in zip(self.scripts, self.configs):
                ack = await remote.cmd_add.set_start(
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
            # Resume the ScriptQueue to begin script execution.
            await remote.cmd_resume.set_start(timeout=10)
            # Wait for the scripts to complete
            print("Waiting for scripts to complete...")
            for script in script_indexes:
                state = await self.wait_for_script_done(remote, script)
                try:
                    script_states.append(int(state))
                except Exception:
                    print("Something went wrong.")
            # Print script indexes
            print(
                f"Scripts complete.\nScript Indexes ; Script States:\n{script_indexes}\n{script_states}"
            )
