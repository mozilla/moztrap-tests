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
    def test_that_user_can_pass_test(self, mozwebqa_logged_in, product, element):
        run_tests_pg = MozTrapRunTestsPage(mozwebqa_logged_in)

        case = self.create_and_run_test(mozwebqa_logged_in, product, element)

        Assert.false(run_tests_pg.is_test_passed(case_name=case['name']))

        run_tests_pg.pass_test(case_name=case['name'])

        Assert.true(run_tests_pg.is_test_passed(case_name=case['name']))

    @pytest.mark.moztrap(206)
    def test_that_user_can_fail_test(self, mozwebqa_logged_in, product, element):
        run_tests_pg = MozTrapRunTestsPage(mozwebqa_logged_in)

        case = self.create_and_run_test(mozwebqa_logged_in, product, element)

        Assert.false(run_tests_pg.is_test_failed(case_name=case['name']))

        run_tests_pg.fail_test(case_name=case['name'])

        Assert.true(run_tests_pg.is_test_failed(case_name=case['name']))

    @pytest.mark.moztrap(207)
    def test_that_user_can_mark_test_invalid(self, mozwebqa_logged_in, product, element):
        run_tests_pg = MozTrapRunTestsPage(mozwebqa_logged_in)

        case = self.create_and_run_test(mozwebqa_logged_in, product, element)

        Assert.false(run_tests_pg.is_test_invalid(case_name=case['name']))

        run_tests_pg.mark_test_invalid(case_name=case['name'])

        Assert.true(run_tests_pg.is_test_invalid(case_name=case['name']))

    @pytest.mark.moztrap(2744)
    def test_that_test_run_saves_right_order_of_test_cases(self, mozwebqa_logged_in, product, element):
        self.connect_product_to_element(mozwebqa_logged_in, product, element)
        version = product['version']
        #create several test case via bulk create
        cases = self.create_bulk_cases(mozwebqa_logged_in, cases_amount=5, product=product, name='is')
        #create first test suite
        suite_a_cases = (cases[3]['name'], cases[1]['name'])
        suite_a = self.create_suite(
            mozwebqa_logged_in, product=product, use_API=True, name='suite A', case_name_list=suite_a_cases)
        #create second test suite
        suite_b_cases = (cases[2]['name'], cases[0]['name'], cases[4]['name'])
        suite_b = self.create_suite(
            mozwebqa_logged_in, product=product, use_API=True, name='suite B', case_name_list=suite_b_cases)
        #create first test run (suite a, suite b)
        first_suite_order = (suite_a['name'], suite_b['name'])
        first_run = self.create_run(
            mozwebqa_logged_in, product=product, activate=True,
            version=version, suite_name_list=first_suite_order)
        #execute first test run
        home_page = MozTrapHomePage(mozwebqa_logged_in)
        home_page.go_to_home_page()
        home_page.go_to_run_test(
            product_name=product['name'], version_name=version['name'], run_name=first_run['name'],
            env_category_name=element['category']['name'], env_element_name=element['name'])

        run_tests_pg = MozTrapRunTestsPage(mozwebqa_logged_in)
        actual_order = [(item.name, item.suite_name) for item in run_tests_pg.test_items]

        expected_order = [(case, suite) for case in suite_a_cases for suite in (suite_a['name'],)] + \
                         [(case, suite) for case in suite_b_cases for suite in (suite_b['name'],)]
        #assert that right order saved
        Assert.equal(actual_order, expected_order)
        #edit run to reorder suites
        manage_runs_pg = MozTrapManageRunsPage(mozwebqa_logged_in)
        manage_runs_pg.go_to_manage_runs_page()
        #push run into draft mode
        manage_runs_pg.filter_form.filter_by(lookup='name', value=first_run['name'])
        manage_runs_pg.make_run_draft(first_run['name'])
        #go to edit run page and reorder suites by name (suite b, suite a)
        edit_run_pg = manage_runs_pg.go_to_edit_run_page(first_run['name'])
        second_run = edit_run_pg.edit_run(first_run, reorder_suites=True)
        #make run active again
        manage_runs_pg.filter_form.filter_by(lookup='name', value=first_run['name'])
        manage_runs_pg.activate_run(first_run['name'])
        #execute run again
        home_page.go_to_home_page()
        home_page.go_to_run_test(
            product_name=product['name'], version_name=version['name'], run_name=first_run['name'],
            env_category_name=element['category']['name'], env_element_name=element['name'])
        #check actual order of items on run tests page
        actual_order = [(item.name, item.suite_name) for item in run_tests_pg.test_items]

        expected_order = [(case, suite) for case in suite_b_cases for suite in (suite_b['name'],)] + \
                         [(case, suite) for case in suite_a_cases for suite in (suite_a['name'],)]
        #assert that right order saved
        Assert.equal(actual_order, expected_order)

    @pytest.mark.moztrap(3302)
    def test_for_edit_active_run_that_includes_suites_to_be_sure_they_are_listed(self, mozwebqa_logged_in, product):
        #create version
        version = product['version']
        #create two test suites
        # TODO: Replace this create suite with API call
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
        manage_runs_pg.filter_form.filter_by(lookup='name', value=test_run['name'])
        test_run = manage_runs_pg.test_runs[0]
        test_run.show_details()

        #assert that order of suites is still correct
        Assert.equal(
            suite_order, test_run.included_suites,
            u'suites are listed in wrong order')
