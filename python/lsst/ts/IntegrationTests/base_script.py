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

    async def run(self) -> None:
        """Run the specified standard or external script."""
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
            for script, config in zip(self.scripts, self.configs):
                await remote.cmd_add.set_start(
                    timeout=10,
                    isStandard=script[1],
                    path=script[0],
                    config=config,
                    logLevel=10,
                    location=queue_placement,
                )
            # Resume the ScriptQueue to begin script execution.
            await remote.cmd_resume.set_start(timeout=10)
