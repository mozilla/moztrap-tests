#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.base_test import BaseTest
from pages.home_page import MozTrapHomePage
from pages.run_tests_page import MozTrapRunTestsPage
from pages.manage_runs_page import MozTrapManageRunsPage


class TestRunTestsPage(BaseTest):

    @pytest.mark.moztrap([205, 208])
    def test_that_user_can_pass_test(self, api, mozwebqa, login, product, element):
        case = self.create_and_run_test(api, mozwebqa, product, element)[0]

        run_tests_pg = MozTrapRunTestsPage(mozwebqa)
        result = run_tests_pg.get_test_result(case['name'])
        Assert.false(result.is_test_passed)

        result.pass_test()

        result = run_tests_pg.get_test_result(case['name'])
        Assert.true(result.is_test_passed)

    @pytest.mark.moztrap(206)
    def test_that_user_can_fail_test(self, api, mozwebqa, login, product, element):
        case = self.create_and_run_test(api, mozwebqa, product, element)[0]

        run_tests_pg = MozTrapRunTestsPage(mozwebqa)
        result = run_tests_pg.get_test_result(case['name'])
        Assert.false(result.is_test_failed)

        result.fail_test()

        result = run_tests_pg.get_test_result(case['name'])
        Assert.true(result.is_test_failed)

    @pytest.mark.moztrap(207)
    def test_that_user_can_mark_test_invalid(self, api, mozwebqa, login, product, element):
        case = self.create_and_run_test(api, mozwebqa, product, element)[0]

        run_tests_pg = MozTrapRunTestsPage(mozwebqa)
        result = run_tests_pg.get_test_result(case['name'])
        Assert.false(result.is_test_invalid)

        result.invalidate_test()

        result = run_tests_pg.get_test_result(case['name'])
        Assert.true(result.is_test_invalid)

    @pytest.mark.moztrap(2744)
    def test_that_test_run_saves_right_order_of_test_cases(self, api, mozwebqa, login, product, element):
        self.connect_product_to_element(mozwebqa, product, element)
        version = product['version']
        # create several test case via bulk create
        cases = self.create_bulk_cases(mozwebqa, product, api=api, cases_amount=5)
        # create first test suite
        suite_a_cases = (cases[3], cases[1])
        suite_a = self.create_suite(
            mozwebqa, product=product, api=api, name='suite A', case_list=suite_a_cases)
        # create second test suite
        suite_b_cases = (cases[2], cases[0], cases[4])
        suite_b = self.create_suite(
            mozwebqa, product=product, api=api, name='suite B', case_list=suite_b_cases)
        # create first test run (suite a, suite b)
        first_suite_order = (suite_a['name'], suite_b['name'])
        first_run = self.create_run(
            mozwebqa, product=product, activate=True,
            version=version, suite_name_list=first_suite_order)
        # execute first test run
        home_page = MozTrapHomePage(mozwebqa)
        home_page.go_to_home_page()
        home_page.go_to_run_test(
            product_name=product['name'], version_name=version['name'], run_name=first_run['name'],
            env_category_name=element['category']['name'], env_element_name=element['name'])

        run_tests_pg = MozTrapRunTestsPage(mozwebqa)
        actual_order = [(item.case_name, item.suite_name) for item in run_tests_pg.test_results]

        expected_order = [(case['name'], suite) for case in suite_a_cases for suite in (suite_a['name'],)] + \
                         [(case['name'], suite) for case in suite_b_cases for suite in (suite_b['name'],)]
        # assert that right order saved
        Assert.equal(actual_order, expected_order)
        # edit run to reorder suites
        manage_runs_pg = MozTrapManageRunsPage(mozwebqa)
        manage_runs_pg.go_to_manage_runs_page()
        # push run into draft mode
        manage_runs_pg.filter_form.filter_by(lookup='name', value=first_run['name'])
        manage_runs_pg.make_run_draft(first_run['name'])
        # go to edit run page and reorder suites by name (suite b, suite a)
        edit_run_pg = manage_runs_pg.go_to_edit_run_page(first_run['name'])
        edit_run_pg.edit_run(first_run, reorder_suites=True)
        # make run active again
        manage_runs_pg.activate_run(first_run['name'])
        # execute run again
        home_page.go_to_home_page()
        home_page.go_to_run_test(
            product_name=product['name'], version_name=version['name'], run_name=first_run['name'],
            env_category_name=element['category']['name'], env_element_name=element['name'])
        # check actual order of items on run tests page
        actual_order = [(item.case_name, item.suite_name) for item in run_tests_pg.test_results]

        expected_order = [(case['name'], suite) for case in suite_b_cases for suite in (suite_b['name'],)] + \
                         [(case['name'], suite) for case in suite_a_cases for suite in (suite_a['name'],)]
        # assert that right order saved
        Assert.equal(actual_order, expected_order)

    def test_that_user_can_mark_test_as_blocked(self, api, mozwebqa, login, product, element):
        case = self.create_and_run_test(api, mozwebqa, product, element)[0]

        run_tests_pg = MozTrapRunTestsPage(mozwebqa)
        test_result = run_tests_pg.get_test_result(case['name'])
        Assert.false(test_result.is_blocked)

        test_result.mark_blocked()

        test_result = run_tests_pg.get_test_result(case['name'])
        Assert.true(test_result.is_blocked)

    def test_that_user_can_skip_test(self, api, mozwebqa, login, product, element):
        case = self.create_and_run_test(api, mozwebqa, product, element)[0]

        run_tests_pg = MozTrapRunTestsPage(mozwebqa)
        test_result = run_tests_pg.get_test_result(case['name'])
        Assert.false(test_result.is_skipped)

        test_result.skip_test()

        test_result = run_tests_pg.get_test_result(case['name'])
        Assert.true(test_result.is_skipped)
