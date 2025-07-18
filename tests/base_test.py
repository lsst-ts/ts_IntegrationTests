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

import os
import unittest

from lsst.ts import salobj
from lsst.ts.IntegrationTests import ScriptQueueController
from lsst.ts.salobj.delete_topics import DeleteTopics, DeleteTopicsArgs
from lsst.ts.xml import subsystems


class BaseTestClass(unittest.IsolatedAsyncioTestCase):
    """
    Defines the common attributes and functions for the unit tests.

    Notes
    -----
    Use index=1 for MainTel, 2 for AuxTel or 3 for OCS
    (Observatory Control System) ScriptQueue. The index is defined as
    a class attribute for simplicity. The sub-Classes define which index,
    if necessary.
    The BaseTest class defaults to index=1, as the most common option.

    Attributes
    ----------
    index : `int`
        The index represents the ScriptQueue for Main Telescope, index=1,
        the Auxilliary Telescope, index=2, or OCS, index=3.

    """

    # See Attributes for the definition.
    index: int = 1

    async def asyncSetUp(self) -> None:
        # Define LSST_TOPIC_SUBNAME.
        salobj.set_test_topic_subname()

        # Create the ScriptQueue Controller.
        self.controller = ScriptQueueController(index=self.index)

        # Start the controller and wait for it be ready.
        await self.controller.start_task

    async def asyncTearDown(self) -> None:
        # Close the controller.
        await self.controller.close()
        await self.controller.done_task

        # Cleanup topics
        topic_subname = os.environ["LSST_TOPIC_SUBNAME"]

        delete_topics = await DeleteTopics.new()

        delete_topics_args = DeleteTopicsArgs(
            all_topics=False,
            subname=topic_subname,
            force=False,
            dry=False,
            log_level=None,
            components=subsystems,
        )

        delete_topics.execute(delete_topics_args)
