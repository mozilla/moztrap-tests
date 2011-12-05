#!/usr/bin/env python
#
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Case Conductor
#
# The Initial Developer of the Original Code is
# Mozilla Corp.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Jonny Gerig Meyer <jonny@oddbird.net>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

from create_cycle_page import CaseConductorCreateCyclePage
from manage_cycles_page import CaseConductorManageCyclesPage
from base_test import BaseTest
from unittestzero import Assert


class TestManageCyclesPage(BaseTest):

    def test_that_user_can_create_and_delete_cycle(self, mozwebqa_logged_in):
        manage_cycles_pg = CaseConductorManageCyclesPage(mozwebqa_logged_in)
        create_cycle_pg = CaseConductorCreateCyclePage(mozwebqa_logged_in)

        product = self.create_product(mozwebqa_logged_in)

        create_cycle_pg.go_to_create_cycle_page()

        cycle = create_cycle_pg.create_cycle(product=product['name'])

        manage_cycles_pg.filter_cycles_by_name(name=cycle['name'])

        Assert.true(manage_cycles_pg.is_element_present(cycle['locator']))

        manage_cycles_pg.delete_cycle(name=cycle['name'])

        Assert.false(manage_cycles_pg.is_element_present(cycle['locator']))

        self.delete_product(mozwebqa_logged_in, product)

    def test_that_user_can_filter_cycle_by_name(self, mozwebqa_logged_in):
        manage_cycles_pg = CaseConductorManageCyclesPage(mozwebqa_logged_in)
        create_cycle_pg = CaseConductorCreateCyclePage(mozwebqa_logged_in)

        product = self.create_product(mozwebqa_logged_in)

        create_cycle_pg.go_to_create_cycle_page()

        cycle = create_cycle_pg.create_cycle(product=product["name"])

        manage_cycles_pg.filter_cycles_by_name(name="Another Cycle")

        Assert.false(manage_cycles_pg.is_element_present(cycle["locator"]))

        manage_cycles_pg.remove_name_filter(name="Another Cycle")
        manage_cycles_pg.filter_cycles_by_name(name=cycle["name"])

        Assert.true(manage_cycles_pg.is_element_present(cycle["locator"]))

        manage_cycles_pg.delete_cycle(name=cycle["name"])

        self.delete_product(mozwebqa_logged_in, product)

    def test_that_user_can_clone_cycle(self, mozwebqa_logged_in):
        manage_cycles_pg = CaseConductorManageCyclesPage(mozwebqa_logged_in)
        create_cycle_pg = CaseConductorCreateCyclePage(mozwebqa_logged_in)

        product = self.create_product(mozwebqa_logged_in)

        create_cycle_pg.go_to_create_cycle_page()

        cycle = create_cycle_pg.create_cycle(product=product['name'])

        manage_cycles_pg.filter_cycles_by_name(name=cycle['name'])

        cloned_cycle = manage_cycles_pg.clone_cycle(name=cycle['name'])

        Assert.true(manage_cycles_pg.is_element_present(cloned_cycle['locator']))

        manage_cycles_pg.delete_cycle(name=cloned_cycle['name'])

        Assert.false(manage_cycles_pg.is_element_present(cloned_cycle['locator']))

        manage_cycles_pg.delete_cycle(name=cycle['name'])

        self.delete_product(mozwebqa_logged_in, product)
