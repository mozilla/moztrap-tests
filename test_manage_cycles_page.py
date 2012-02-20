#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from manage_cycles_page import CaseConductorManageCyclesPage
from base_test import BaseTest
from unittestzero import Assert


class TestManageCyclesPage(BaseTest):

    def test_that_user_can_create_and_delete_cycle(self, mozwebqa_logged_in):
        manage_cycles_pg = CaseConductorManageCyclesPage(mozwebqa_logged_in)

        cycle = self.create_cycle(mozwebqa_logged_in)

        manage_cycles_pg.filter_cycles_by_name(name=cycle['name'])

        Assert.true(manage_cycles_pg.is_element_present(cycle['manage_locator']))

        manage_cycles_pg.delete_cycle(name=cycle['name'])

        Assert.false(manage_cycles_pg.is_element_present(cycle['manage_locator']))

        self.delete_product(mozwebqa_logged_in, cycle['product'])

    def test_that_user_can_filter_cycle_by_name(self, mozwebqa_logged_in):
        manage_cycles_pg = CaseConductorManageCyclesPage(mozwebqa_logged_in)

        cycle = self.create_cycle(mozwebqa_logged_in)

        manage_cycles_pg.filter_cycles_by_name(name='Another Cycle')

        Assert.false(manage_cycles_pg.is_element_present(cycle['manage_locator']))

        manage_cycles_pg.remove_name_filter(name='Another Cycle')
        manage_cycles_pg.filter_cycles_by_name(name=cycle['name'])

        Assert.true(manage_cycles_pg.is_element_present(cycle['manage_locator']))

        self.delete_cycle(mozwebqa_logged_in, cycle, delete_product=True)

    def test_that_user_can_clone_cycle(self, mozwebqa_logged_in):
        manage_cycles_pg = CaseConductorManageCyclesPage(mozwebqa_logged_in)

        cycle = self.create_cycle(mozwebqa_logged_in)

        manage_cycles_pg.filter_cycles_by_name(name=cycle['name'])

        cloned_cycle = manage_cycles_pg.clone_cycle(name=cycle['name'])

        Assert.true(manage_cycles_pg.is_element_present(cloned_cycle['manage_locator']))

        manage_cycles_pg.delete_cycle(name=cloned_cycle['name'])

        Assert.false(manage_cycles_pg.is_element_present(cloned_cycle['manage_locator']))

        self.delete_cycle(mozwebqa_logged_in, cycle, delete_product=True)
