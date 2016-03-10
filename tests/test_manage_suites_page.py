# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

import pytest

from pages.base_test import BaseTest
from pages.manage_suites_page import MozTrapManageSuitesPage


class TestManageSuitesPage(BaseTest):

    @pytest.mark.moztrap([98, 99])
    def test_that_user_can_create_and_delete_suite(self, base_url, selenium, login, product):
        manage_suites_pg = MozTrapManageSuitesPage(base_url, selenium)

        suite = self.create_suite(base_url, selenium, product)

        manage_suites_pg.filter_form.filter_by(lookup='name', value=suite['name'])

        assert manage_suites_pg.is_element_present(*suite['locator'])

        manage_suites_pg.delete_suite(name=suite['name'])

        assert not manage_suites_pg.is_element_present(*suite['locator'])

    def test_that_user_can_create_suite_and_add_some_cases_to_it(self, api, base_url, selenium, login, product):
        manage_suites_pg = MozTrapManageSuitesPage(base_url, selenium)

        cases = [self.create_case(base_url, selenium, product=product, api=api) for i in range(3)]
        suite = self.create_suite(base_url, selenium, product=product, api=api, case_list=[case for case in cases])

        manage_suites_pg.go_to_manage_suites_page()
        manage_suites_pg.filter_form.filter_by(lookup='name', value=suite['name'])
        assert manage_suites_pg.is_suite_present(suite)

        manage_test_cases_pg = manage_suites_pg.view_cases(name=suite['name'])

        for case in cases:
            assert manage_test_cases_pg.is_case_present(case)

    @pytest.mark.moztrap(2743)
    def test_editing_of_existing_suite_that_has_no_included_cases(self, api, base_url, selenium, login, product):
        # create suite and cases
        suite = self.create_suite(base_url, selenium, product, api=api)
        cases = self.create_bulk_cases(base_url, selenium, product, api=api, cases_amount=3)

        # simulate random order of cases
        case_list = [cases[i]['name'] for i in (2, 0, 1)]

        manage_suites_pg = MozTrapManageSuitesPage(base_url, selenium)
        manage_suites_pg.go_to_manage_suites_page()
        manage_suites_pg.filter_form.filter_by(lookup='name', value=suite['name'])
        edit_suite_pg = manage_suites_pg.edit_suite(name=suite['name'])

        # product field should not be read-only.
        assert not edit_suite_pg.is_product_field_readonly

        edit_suite_pg.include_cases_to_suite(case_list)

        edit_suite_pg = manage_suites_pg.edit_suite(name=suite['name'])

        assert edit_suite_pg.is_product_field_readonly
        assert case_list == [item.name for item in edit_suite_pg.included_cases]

    @pytest.mark.moztrap(2742)
    def test_editing_of_existing_suite_that_includes_cases(self, api, base_url, selenium, login, product):
        # create suite and cases (both included and not included into suite)
        included_cases = self.create_bulk_cases(base_url, selenium, product, api=api, cases_amount=2)
        not_included_cases = self.create_bulk_cases(base_url, selenium, product, api=api, cases_amount=3)
        suite = self.create_suite(base_url, selenium, product, api=api, case_list=[case for case in included_cases])

        # filter by suite name and go to edit suite page
        manage_suites_pg = MozTrapManageSuitesPage(base_url, selenium)
        manage_suites_pg.go_to_manage_suites_page()
        manage_suites_pg.filter_form.filter_by(lookup='name', value=suite['name'])
        edit_suite_pg = manage_suites_pg.edit_suite(name=suite['name'])

        assert edit_suite_pg.is_product_field_readonly

        # check list of available cases
        actual_available_cases = [item.name for item in edit_suite_pg.available_cases]
        expected_available_cases = [item['name'] for item in not_included_cases]
        assert expected_available_cases == actual_available_cases

        # check list of included cases
        actual_included_cases = [item.name for item in edit_suite_pg.included_cases]
        expected_included_cases = [item['name'] for item in included_cases]
        assert expected_included_cases == actual_included_cases

        # get all cases names and make random order via random.shuffle
        all_cases = expected_available_cases + expected_included_cases
        random.shuffle(all_cases)

        # include cases to suite in the expected order
        edit_suite_pg.remove_all_included_cases()
        edit_suite_pg.include_cases_to_suite(all_cases)

        # re-edit the same suite
        edit_suite_pg = manage_suites_pg.edit_suite(name=suite['name'])

        # and ensure that included cases are listed in right order
        assert all_cases == [item.name for item in edit_suite_pg.included_cases]
