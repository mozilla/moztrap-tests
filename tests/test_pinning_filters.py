#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.base_test import BaseTest
from pages.manage_runs_page import MozTrapManageRunsPage
from pages.manage_cases_page import MozTrapManageCasesPage
from pages.manage_suites_page import MozTrapManageSuitesPage
from pages.manage_versions_page import MozTrapManageVersionsPage
from pages.view_run_results_page import MozTrapViewRunResultsPage


class TestPinningFilters(BaseTest):

    @pytest.mark.moztrap(5935)
    def test_that_pinning_filter_on_product_version_set_defaults_in_new_run(self, mozwebqa, login, product):
        product_version_name = u'%s %s' % (product['name'], product['version']['name'])

        manage_runs_pg = MozTrapManageRunsPage(mozwebqa)
        manage_runs_pg.go_to_manage_runs_page()
        filter_item = manage_runs_pg.filter_form.filter_by(lookup='productversion', value=product_version_name)

        # check that filter is not orange before it's pinned
        self.check_pinned_filter(filter_item, is_pinned=False)
        filter_item.pin_filter()

        # check that filter is orange after it's been pinned
        self.check_pinned_filter(filter_item, is_pinned=True)

        create_run_pg = manage_runs_pg.click_create_run_button()

        Assert.equal(
            create_run_pg.product_version_value,
            product_version_name,
            u'default product version is incorrect')

    @pytest.mark.moztrap(5930)
    def test_that_pinning_name_field_filter_only_works_for_current_page(self, api, mozwebqa, login, product):
        good_case_name = u'mozilla'
        good_suite_name = u'MozTrap'

        self.create_bulk_cases(mozwebqa, product, api=api, name=good_case_name, cases_amount=3)
        self.create_bulk_cases(mozwebqa, product, api=api, name=u'ALLIZOM', cases_amount=2)
        self.create_suite(mozwebqa, product, api=api, name=good_suite_name)
        self.create_suite(mozwebqa, product, api=api, name=u'PartZom')

        manage_cases_pg = MozTrapManageCasesPage(mozwebqa)
        manage_cases_pg.go_to_manage_cases_page()

        # filter cases by name and assert that only cases with mozilla in their name are found
        cases_filter = manage_cases_pg.filter_form.filter_by(lookup='name', value=good_case_name)
        Assert.equal(cases_filter.content_text, good_case_name)
        self.check_pinned_filter(cases_filter, is_pinned=False)
        for case in manage_cases_pg.test_cases:
            Assert.contains(good_case_name, case.name.lower())

        # pin filter and assert that it turns orange
        cases_filter.pin_filter()
        self.check_pinned_filter(cases_filter, is_pinned=True)

        manage_suites_pg = MozTrapManageSuitesPage(mozwebqa)
        manage_suites_pg.go_to_manage_suites_page()

        # check that there is no filters applied
        Assert.equal(manage_suites_pg.filter_form.filter_items, [])

        # filter suites by name and assert that only suites with moztrap in their name are found
        suites_filter = manage_suites_pg.filter_form.filter_by(lookup='name', value=good_suite_name)
        Assert.equal(suites_filter.content_text, good_suite_name.lower())
        self.check_pinned_filter(suites_filter, is_pinned=False)
        for suite in manage_suites_pg.test_suites:
            Assert.contains(good_suite_name, suite.name)

        # pin filter and assert that it turns orange
        suites_filter.pin_filter()
        self.check_pinned_filter(suites_filter, is_pinned=True)

        # and check everything again on manage cases page
        manage_cases_pg.go_to_manage_cases_page()
        applied_filter = manage_cases_pg.filter_form.filter_items
        Assert.equal(len(applied_filter), 1)
        Assert.equal(applied_filter[0].content_text, good_case_name)
        for case in manage_cases_pg.test_cases:
            Assert.contains(good_case_name, case.name.lower())

        # and check everything one more time on manage suites page
        manage_suites_pg.go_to_manage_suites_page()
        applied_filter = manage_suites_pg.filter_form.filter_items
        Assert.equal(len(applied_filter), 1)
        Assert.equal(applied_filter[0].content_text, good_suite_name.lower())
        for suite in manage_suites_pg.test_suites:
            Assert.contains(good_suite_name, suite.name)

        # and go to manage runs page and see no filters there
        manage_runs_pg = MozTrapManageRunsPage(mozwebqa)
        manage_runs_pg.go_to_manage_runs_page()

        # check that there is no filters applied
        Assert.equal(manage_runs_pg.filter_form.filter_items, [])

    @pytest.mark.moztrap(5933)
    def test_that_pinning_filters_on_product_sets_defaults_in_new_suite(self, mozwebqa, login, product):
        manage_suites_pg = MozTrapManageSuitesPage(mozwebqa)
        manage_suites_pg.go_to_manage_suites_page()
        filter_item = manage_suites_pg.filter_form.filter_by(lookup='product', value=product['name'])

        # check that filter is not orange before it's pinned
        self.check_pinned_filter(filter_item, is_pinned=False)
        filter_item.pin_filter()

        # check that filter is orange after it's been pinned
        self.check_pinned_filter(filter_item, is_pinned=True)

        create_suite_pg = manage_suites_pg.click_create_suite_button()

        Assert.equal(
            create_suite_pg.product_name_value,
            product['name'],
            u'default product is incorrect')

    @pytest.mark.moztrap(5932)
    @pytest.mark.xfail(reason='Bug 1008850 - Suggestion box is cut off when the filter is too long')
    def test_that_pinning_filters_on_product_and_version_and_suite_set_defaults_in_new_case(self, api, mozwebqa, login, product):
        version = product['version']
        product_version_name = u'%s %s' % (product['name'], version['name'])
        suite = self.create_suite(mozwebqa, product=product, api=api)

        manage_cases_pg = MozTrapManageCasesPage(mozwebqa)
        manage_cases_pg.go_to_manage_cases_page()

        filters = []
        filters.append(manage_cases_pg.filter_form.filter_by(lookup='product', value=product['name']))
        filters.append(manage_cases_pg.filter_form.filter_by(lookup='productversion', value=product_version_name))
        filters.append(manage_cases_pg.filter_form.filter_by(lookup='suite', value=suite['name']))

        for item in filters:
            item.pin_filter()
            self.check_pinned_filter(item, is_pinned=True)

        # go to create case page
        create_case_pg = manage_cases_pg.click_create_case_button()
        Assert.equal(create_case_pg.product_value, product['name'])
        Assert.equal(create_case_pg.product_version_value, version['name'])
        Assert.equal(create_case_pg.suite_value, suite['name'])

        create_case_pg.go_back()

        # go to create bulk cases page
        create_bulk_cases_pg = manage_cases_pg.click_create_bulk_cases_button()
        Assert.equal(create_bulk_cases_pg.product_value, product['name'])
        Assert.equal(create_bulk_cases_pg.product_version_value, version['name'])
        Assert.equal(create_bulk_cases_pg.suite_value, suite['name'])

    @pytest.mark.moztrap(5936)
    def test_that_pinning_filter_on_product_sets_defaults_in_new_product_version(self, mozwebqa, login, product):
        manage_versions_pg = MozTrapManageVersionsPage(mozwebqa)
        manage_versions_pg.go_to_manage_versions_page()
        filter_item = manage_versions_pg.filter_form.filter_by(lookup='product', value=product['name'])

        # check that filter is not orange before it's pinned
        self.check_pinned_filter(filter_item, is_pinned=False)
        filter_item.pin_filter()

        # check that filter is orange after it's been pinned
        self.check_pinned_filter(filter_item, is_pinned=True)

        create_version_pg = manage_versions_pg.click_create_version_button()

        Assert.equal(
            create_version_pg.product_name_value,
            product['name'],
            u'default product is incorrect')

    @pytest.mark.moztrap(5931)
    def test_that_pinning_filter_persists_for_session(self, api, mozwebqa, existing_user, login, product, element):
        # create suite, cases and test run
        product_version_name = u'%s %s' % (product['name'], product['version']['name'])
        case, suite, run = self.create_and_run_test(api, mozwebqa, product, element)

        # go to manage cases page
        manage_cases_pg = MozTrapManageCasesPage(mozwebqa)
        manage_cases_pg.go_to_manage_cases_page()

        # filter on product
        filter_item = manage_cases_pg.filter_form.filter_by(lookup='product', value=product['name'])
        self.check_pinned_filter(filter_item, is_pinned=False)

        # see only cases for specified product
        displayed_cases = manage_cases_pg.test_cases
        Assert.equal(len(displayed_cases), 1, 'there should be only one case displayed')
        Assert.equal(case.name.lower(), displayed_cases[0].name.lower(),
                     'displayed case name differs from expected value')

        # pin product filter
        filter_item.pin_filter()
        self.check_pinned_filter(filter_item, is_pinned=True)

        # go to manage suites page
        manage_suites_pg = MozTrapManageSuitesPage(mozwebqa)
        manage_suites_pg.go_to_manage_suites_page()

        # see only suites for specified product
        displayed_suites = manage_suites_pg.test_suites
        Assert.equal(len(displayed_suites), 1, 'there should be only one suite displayed')
        Assert.equal(suite.name.lower(), displayed_suites[0].name.lower(),
                     'displayed suite name differs from expected value')

        # go to results page
        view_results_pg = MozTrapViewRunResultsPage(mozwebqa)
        view_results_pg.go_to_view_run_results_page()

        # see only results for specified product
        # because we are going to check the same thing several times
        # let's define a function and call it each time we need this check

        def check_test_run_results(results):
            Assert.equal(len(results), 1, 'there should be only one test run result')
            Assert.equal(run['name'].lower(), results[0].name.lower(),
                         'displayed run name differs from expected value')
            Assert.equal(product_version_name, results[0].product_version,
                         'displayed test run productversion differs from expected value')

        check_test_run_results(view_results_pg.test_run_results)

        # refresh page and see that filter persists
        view_results_pg.refresh()
        check_test_run_results(view_results_pg.test_run_results)

        # log out and back in and see that filter persists
        view_results_pg.header.click_logout()
        view_results_pg.header.login(existing_user['email'], existing_user['password'])
        check_test_run_results(view_results_pg.test_run_results)

        # check that filter is still pinned
        filters = view_results_pg.filter_form.filter_items
        Assert.equal(len(filters), 1)
        self.check_pinned_filter(filters[0], is_pinned=True)

    def check_pinned_filter(self, filter_item, is_pinned):
        pinned_filter_color = u'#DFB081'
        if is_pinned:
            # check that filter is orange after it's been pinned
            Assert.equal(
                filter_item.get_filter_color(),
                pinned_filter_color,
                u'pinned filter\'s color is not orange')
        else:
            # check that filter is not orange before it's pinned
            Assert.not_equal(
                filter_item.get_filter_color(),
                pinned_filter_color,
                u'filter is orange before it was pinned')
