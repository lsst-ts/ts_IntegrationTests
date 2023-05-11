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

import asyncio
from .script_queue_controller import ScriptQueueController
from lsst.ts.idl.enums.ScriptQueue import ScriptProcessState


# Create an inherited class from the controller,
# so that you can add logic when commands are received.
# You can also output events and telemetry from there.
class FailingScriptQueueController(ScriptQueueController):
    """Define a ScriptQueue controller to use for scripts going into
    failed states. This is used by certain unit tests to
    mimic the functions of the real ScriptQueue, to verify
    integration test scripts that fail for various reasons.
    """

    def __init__(self, index: int, test_type: str) -> None:
        """Initialize the Failing ScriptQueue Controller.

        Parameters
        ----------
        index : `int`
            Defines whether this is a MainTel (index=1)
            or an AuxTel (index=2) controller.
        test_type : `str`
            Defines what type of failing test to mimic.
        """
        super().__init__(index)
        self.test_type: str = test_type

    async def do_resume(self, data: tuple) -> None:
        """Resume the ScriptQueue after adding the scripts
        to the queue. The ScriptQueue will then execute
        the scripts.

        """
        # self.log.info("ScriptQueue resumed\n")
        for script, _ in enumerate(self.queue_list, start=1):
            await self.evt_script.set_write(
                scriptSalIndex=script,
                processState=ScriptProcessState.RUNNING,
                scriptState=3,  # RUNNING
            )
            await asyncio.sleep(0.1)
            if self.test_type.upper() == "TERMINATED":
                await self.evt_script.set_write(
                    scriptSalIndex=script,
                    processState=ScriptProcessState.TERMINATED,
                    # The next line is technically improper,
                    # but for testing, it's fine.
                    scriptState=ScriptProcessState.TERMINATED,
                    timestampProcessEnd=99999,
                )
            elif self.test_type.upper() == "FAILED":
                await self.evt_script.set_write(
                    scriptSalIndex=script,
                    processState=ScriptProcessState.DONE,
                    scriptState=10,  # FAILED
                    timestampProcessEnd=99999,
                )
            else:
                await self.evt_script.set_write(
                    scriptSalIndex=script,
                    processState=ScriptProcessState.DONE,
                    timestampProcessEnd=99999,
                )
