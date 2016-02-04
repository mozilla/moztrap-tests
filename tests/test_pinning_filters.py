# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

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

        assert product_version_name == create_run_pg.product_version_value

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
        assert good_case_name == cases_filter.content_text
        self.check_pinned_filter(cases_filter, is_pinned=False)
        for case in manage_cases_pg.test_cases:
            assert good_case_name in case.name.lower()

        # pin filter and assert that it turns orange
        cases_filter.pin_filter()
        self.check_pinned_filter(cases_filter, is_pinned=True)

        manage_suites_pg = MozTrapManageSuitesPage(mozwebqa)
        manage_suites_pg.go_to_manage_suites_page()

        # check that there is no filters applied
        assert [] == manage_suites_pg.filter_form.filter_items

        # filter suites by name and assert that only suites with moztrap in their name are found
        suites_filter = manage_suites_pg.filter_form.filter_by(lookup='name', value=good_suite_name)
        assert good_suite_name.lower() == suites_filter.content_text
        self.check_pinned_filter(suites_filter, is_pinned=False)
        for suite in manage_suites_pg.test_suites:
            assert good_suite_name in suite.name

        # pin filter and assert that it turns orange
        suites_filter.pin_filter()
        self.check_pinned_filter(suites_filter, is_pinned=True)

        # and check everything again on manage cases page
        manage_cases_pg.go_to_manage_cases_page()
        applied_filter = manage_cases_pg.filter_form.filter_items
        assert 1 == len(applied_filter)
        assert good_case_name == applied_filter[0].content_text
        for case in manage_cases_pg.test_cases:
            assert good_case_name in case.name.lower()

        # and check everything one more time on manage suites page
        manage_suites_pg.go_to_manage_suites_page()
        applied_filter = manage_suites_pg.filter_form.filter_items
        assert 1 == len(applied_filter)
        assert good_suite_name.lower() == applied_filter[0].content_text
        for suite in manage_suites_pg.test_suites:
            assert good_suite_name in suite.name

        # and go to manage runs page and see no filters there
        manage_runs_pg = MozTrapManageRunsPage(mozwebqa)
        manage_runs_pg.go_to_manage_runs_page()

        # check that there is no filters applied
        assert [] == manage_runs_pg.filter_form.filter_items

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

        assert product['name'] == create_suite_pg.product_name_value

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
        assert product['name'] == create_case_pg.product_value
        assert version['name'] == create_case_pg.product_version_value
        assert suite['name'] == create_case_pg.suite_value

        create_case_pg.go_back()

        # go to create bulk cases page
        create_bulk_cases_pg = manage_cases_pg.click_create_bulk_cases_button()
        assert product['name'] == create_bulk_cases_pg.product_value
        assert version['name'] == create_bulk_cases_pg.product_version_value
        assert suite['name'] == create_bulk_cases_pg.suite_value

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

        assert product['name'] == create_version_pg.product_name_value

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
        assert 1 == len(displayed_cases)
        assert case.name.lower() == displayed_cases[0].name.lower()

        # pin product filter
        filter_item.pin_filter()
        self.check_pinned_filter(filter_item, is_pinned=True)

        # go to manage suites page
        manage_suites_pg = MozTrapManageSuitesPage(mozwebqa)
        manage_suites_pg.go_to_manage_suites_page()

        # see only suites for specified product
        displayed_suites = manage_suites_pg.test_suites
        assert 1 == len(displayed_suites)
        assert suite.name.lower() == displayed_suites[0].name.lower()

        # go to results page
        view_results_pg = MozTrapViewRunResultsPage(mozwebqa)
        view_results_pg.go_to_view_run_results_page()

        # see only results for specified product
        # because we are going to check the same thing several times
        # let's define a function and call it each time we need this check

        def check_test_run_results(results):
            assert 1 == len(results)
            assert run['name'].lower() == results[0].name.lower()
            assert product_version_name == results[0].product_version

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
        assert 1 == len(filters)
        self.check_pinned_filter(filters[0], is_pinned=True)

    def check_pinned_filter(self, filter_item, is_pinned):
        pinned_filter_color = u'#DFB081'
        if is_pinned:
            # check that filter is orange after it's been pinned
            assert pinned_filter_color == filter_item.get_filter_color()
        else:
            # check that filter is not orange before it's pinned
            assert not pinned_filter_color == filter_item.get_filter_color()
