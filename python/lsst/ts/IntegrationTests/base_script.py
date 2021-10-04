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


class BaseScript:
    """Integration tests script base class."""

    index = 1

    def __init__(self, config, script, isStandard=True, queue_placement="FIRST"):
        self.config = config
        self.script = script
        self.isStandard = isStandard
        self.queue_placement = queue_placement
        self.start_remote(self.index)

    async def start_remote(self, index=index):
        """Start the ScriptQueue remote and define the domain.

        Parameters
        ----------
        index : integer
            Taking the index as an argument allows this to be called
            with more flexibility.

        """
        async with salobj.Domain() as domain, salobj.Remote(
            domain=domain, name="ScriptQueue", index=self.index
        ) as remote:
            # note: use index=1 for MT, 2 for AuxTel;
            # also since `async with` is used,
            # you do NOT have to wait for the remote to start
            await remote.evt_heartbeat.next(flush=True, timeout=30)

    async def pause_queue(self):
        await remote.cmd_pause.start(timeout=10)

    async def run(self):
        """Run the specified standard or external script."""
        queue_placement = getattr(
            ScriptQueue.Location, self.queue_placement.upper()
        )
        await remote.cmd_add.set_start(
            timeout=10,
            isStandard=self.isStandard,
            path=self.script,
            config=self.config,
            logLevel=10,
            location=queue_placement,
        )
        await remote.cmd_resume.set_start(timeout=10)
        print("You have executed the " + self.script + "script.")
