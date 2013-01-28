#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.base_test import BaseTest
from pages.manage_suites_page import MozTrapManageSuitesPage


class TestManageSuitesPage(BaseTest):

    @pytest.mark.moztrap([98, 99])
    def test_that_user_can_create_and_delete_suite(self, mozwebqa_logged_in):
        manage_suites_pg = MozTrapManageSuitesPage(mozwebqa_logged_in)

        suite = self.create_suite(mozwebqa_logged_in)

        manage_suites_pg.filter_form.filter_by(lookup='name', value=suite['name'])

        Assert.true(manage_suites_pg.is_element_present(*suite['locator']))

        manage_suites_pg.delete_suite(name=suite['name'])

        Assert.false(manage_suites_pg.is_element_present(*suite['locator']))

        self.delete_product(mozwebqa_logged_in, product=suite['product'])

    def test_that_user_can_create_suite_and_add_some_cases_to_it(self, mozwebqa_logged_in):
        manage_suites_pg = MozTrapManageSuitesPage(mozwebqa_logged_in)

        product = self.create_product(mozwebqa_logged_in)
        cases = [self.create_case(mozwebqa=mozwebqa_logged_in, product=product) for i in range(3)]

        suite = self.create_suite(mozwebqa=mozwebqa_logged_in, product=product, case_name_list=[case['name'] for case in cases])

        manage_suites_pg.filter_form.filter_by(lookup='name', value=suite['name'])
        Assert.true(manage_suites_pg.is_element_present(*suite['locator']))

        manage_test_cases_pg = manage_suites_pg.view_cases(name=suite['name'])

        for case in cases:
            Assert.true(manage_test_cases_pg.is_element_present(*case['locator']))

    @pytest.mark.moztrap(2743)
    def test_editing_of_existing_suite_that_has_no_included_cases(self, mozwebqa_logged_in):
        #create product, suite and cases
        product = self.create_product(mozwebqa_logged_in)
        suite = self.create_suite(mozwebqa_logged_in, product=product)
        cases = self.create_bulk_cases(mozwebqa_logged_in, cases_amount=3, product=product)

        #simulate random order of cases
        case_list = [cases[i]['name'] for i in (2, 0, 1)]

        manage_suites_pg = MozTrapManageSuitesPage(mozwebqa_logged_in)
        manage_suites_pg.go_to_manage_suites_page()
        manage_suites_pg.filter_form.filter_by(lookup='name', value=suite['name'])
        edit_suite_pg = manage_suites_pg.edit_suite(name=suite['name'])

        #product field should not be read-only.
        Assert.false(
            edit_suite_pg.is_product_field_readonly,
            u'product version field should be editable')

        edit_suite_pg.include_cases_to_suite(case_list)
        manage_suites_pg.filter_form.filter_by(lookup='name', value=suite['name'])
        edit_suite_pg = manage_suites_pg.edit_suite(name=suite['name'])

        Assert.true(
            edit_suite_pg.is_product_field_readonly,
            u'product version field should be read-only')

        Assert.equal(
            [item.name for item in edit_suite_pg.included_cases], case_list,
            u'items are listed in wrong order')
