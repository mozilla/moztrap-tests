#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.manage_runs_page import MozTrapManageRunsPage
from pages.base_test import BaseTest
from unittestzero import Assert


class TestManageRunsPage(BaseTest):

    def test_that_user_can_create_and_delete_run(self, mozwebqa_logged_in):
        manage_runs_pg = MozTrapManageRunsPage(mozwebqa_logged_in)

        run = self.create_run(mozwebqa_logged_in)

        manage_runs_pg.filter_runs_by_name(name=run['name'])

        Assert.true(manage_runs_pg.is_element_present(run['manage_locator']))

        manage_runs_pg.delete_run(name=run['name'])

        Assert.false(manage_runs_pg.is_element_present(run['manage_locator']))

        self.delete_version(mozwebqa_logged_in, version=run['version'], delete_product=True)
