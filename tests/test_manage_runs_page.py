# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.base_test import BaseTest
from pages.manage_runs_page import MozTrapManageRunsPage


class TestManageRunsPage(BaseTest):

    @pytest.mark.moztrap([113, 112])
    def test_that_user_can_create_and_delete_run(self, mozwebqa, login, product):
        manage_runs_pg = MozTrapManageRunsPage(mozwebqa)

        run = self.create_run(mozwebqa, product=product)

        manage_runs_pg.filter_form.filter_by(lookup='name', value=run['name'])

        assert manage_runs_pg.is_element_present(*run['manage_locator'])

        manage_runs_pg.delete_run(name=run['name'])

        assert not manage_runs_pg.is_element_present(*run['manage_locator'])

    @pytest.mark.moztrap(3302)
    def test_for_edit_active_run_that_includes_suites_to_be_sure_they_are_listed(self, api, mozwebqa, login, product):
        # create version
        version = product['version']
        # create two test suites
        suite_a = self.create_suite(mozwebqa, product=product, api=api, name='suite A')
        suite_b = self.create_suite(mozwebqa, product=product, api=api, name='suite B')
        # create test run
        suite_order = [suite_b['name'], suite_a['name']]
        test_run = self.create_run(
            mozwebqa, product=product,
            version=version, suite_name_list=suite_order)

        manage_runs_pg = MozTrapManageRunsPage(mozwebqa)
        manage_runs_pg.go_to_manage_runs_page()
        manage_runs_pg.filter_form.filter_by(lookup='name', value=test_run['name'])
        manage_runs_pg.activate_run(name=test_run['name'])
        edit_run_pg = manage_runs_pg.go_to_edit_run_page(test_run['name'])

        # assert that multiselect widget is not present thus suites list is readonly
        assert not edit_run_pg.is_multiselect_widget_present
        # assert that order of suites is correct
        assert suite_order == edit_run_pg.readonly_included_suites

        edit_run_pg.save_run()
        test_run = manage_runs_pg.test_runs[0]
        test_run.show_details()

        # assert that order of suites is still correct
        assert suite_order == test_run.included_suites
