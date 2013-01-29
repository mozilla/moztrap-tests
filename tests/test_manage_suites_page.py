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
