#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.base_test import BaseTest
from pages.manage_runs_page import MozTrapManageRunsPage


class TestManageRunsPage(BaseTest):

    @pytest.mark.moztrap([113, 112])
    def test_that_user_can_create_and_delete_run(self, mozwebqa_logged_in, product):
        manage_runs_pg = MozTrapManageRunsPage(mozwebqa_logged_in)

        run = self.create_run(mozwebqa_logged_in, product=product)

        manage_runs_pg.filter_form.filter_by(lookup='name', value=run['name'])

        Assert.true(manage_runs_pg.is_element_present(*run['manage_locator']))

        manage_runs_pg.delete_run(name=run['name'])

        Assert.false(manage_runs_pg.is_element_present(*run['manage_locator']))

    @pytest.mark.moztrap(3302)
    def test_for_edit_active_run_that_includes_suites_to_be_sure_they_are_listed(self, mozwebqa_logged_in, product):
        #create version
        version = product['version']
        #create two test suites
        suite_a = self.create_suite(mozwebqa_logged_in, product=product, use_API=True, name='suite A')
        suite_b = self.create_suite(mozwebqa_logged_in, product=product, use_API=True, name='suite B')
        #create test run
        suite_order = [suite_b['name'], suite_a['name']]
        test_run = self.create_run(
            mozwebqa_logged_in, product=product,
            version=version, suite_name_list=suite_order)

        manage_runs_pg = MozTrapManageRunsPage(mozwebqa_logged_in)
        manage_runs_pg.go_to_manage_runs_page()
        manage_runs_pg.filter_form.filter_by(lookup='name', value=test_run['name'])
        manage_runs_pg.activate_run(name=test_run['name'])
        edit_run_pg = manage_runs_pg.go_to_edit_run_page(test_run['name'])

        #assert that multiselect widget is not present thus suites list is readonly
        Assert.false(
            edit_run_pg.is_multiselect_widget_present,
            u'multiselect widget should not be present')
        #assert that order of suites is correct
        Assert.equal(
            suite_order, edit_run_pg.readonly_included_suites,
            u'suites are listed in wrong order')

        edit_run_pg.save_run()
        test_run = manage_runs_pg.test_runs[0]
        test_run.show_details()

        #assert that order of suites is still correct
        Assert.equal(
            suite_order, test_run.included_suites,
            u'suites are listed in wrong order')
