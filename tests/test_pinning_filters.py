#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert

from pages.base_test import BaseTest
from pages.manage_runs_page import MozTrapManageRunsPage


PINNED_FILTER_COLOR = u'#DFB081'


class TestPinningFilters(BaseTest):

    @pytest.mark.moztrap(5935)
    @pytest.mark.nondestructive
    def test_that_pinning_filter_on_product_version_set_defaults_in_new_run(self, mozwebqa_logged_in):
        product = self.create_product(mozwebqa_logged_in)
        product_version_name = u'%s %s' % (product['name'], product['version']['name'])

        manage_runs_pg = MozTrapManageRunsPage(mozwebqa_logged_in)
        manage_runs_pg.go_to_manage_runs_page()
        filter_item = manage_runs_pg.filter_form.filter_by(
            lookup='productversion', value=product_version_name)

        #check that filter is not orange before it's pinned
        Assert.not_equal(
            filter_item.get_filter_color(),
            PINNED_FILTER_COLOR)

        filter_item.pin_filter()

        #check that filter is orange after it's been pinned
        Assert.equal(
            filter_item.get_filter_color(),
            PINNED_FILTER_COLOR)

        create_run_pg = manage_runs_pg.click_create_run_button()

        Assert.equal(
            create_run_pg.product_version,
            product_version_name)

    @pytest.mark.moztrap(5930)
    @pytest.mark.nondestructive
    def test_that_pinning_name_field_filter_only_works_for_current_page(self, mozwebqa_logged_in):
        good_case_name = u'MOZILLA'
        good_suite_name = u'MozTrap'

        product = self.create_product(mozwebqa_logged_in)
        first_cases_set = self.create_bulk_cases(mozwebqa_logged_in, name=good_case_name, product=product, cases_amount=3)
        second_cases_set = self.create_bulk_cases(mozwebqa_logged_in, name=u'ALLIZOM', product=product, cases_amount=2)
        first_suite = self.create_suite(mozwebqa_logged_in, name=good_suite_name, product=product)
        second_suite = self.create_suite(mozwebqa_logged_in, name=u'PartZom', product=product)

        from pages.manage_cases_page import MozTrapManageCasesPage
        manage_cases_pg = MozTrapManageCasesPage(mozwebqa_logged_in)
        manage_cases_pg.go_to_manage_cases_page()

        #filter cases by name and assert that only cases with mozilla in their name are found
        cases_filter = manage_cases_pg.filter_form.filter_by(lookup='name', value=good_case_name)
        Assert.equal(cases_filter.content_text, good_case_name.lower())
        Assert.not_equal(cases_filter.get_filter_color(), PINNED_FILTER_COLOR)
        for case in manage_cases_pg.test_cases:
            Assert.contains(good_case_name, case.name)

        #pin filter and assert that it turns orange
        cases_filter.pin_filter()
        Assert.equal(cases_filter.get_filter_color(), PINNED_FILTER_COLOR)

        from pages.manage_suites_page import MozTrapManageSuitesPage
        manage_suites_pg = MozTrapManageSuitesPage(mozwebqa_logged_in)
        manage_suites_pg.go_to_manage_suites_page()

        #check that there is no filters applied
        Assert.equal(manage_suites_pg.filter_form.filter_items, [])

        #filter suites by name and assert that only suites with moztrap in their name are found
        suites_filter = manage_suites_pg.filter_form.filter_by(lookup='name', value=good_suite_name)
        Assert.equal(suites_filter.content_text, good_suite_name.lower())
        Assert.not_equal(suites_filter.get_filter_color(), PINNED_FILTER_COLOR)
        for suite in manage_suites_pg.test_suites:
            Assert.contains(good_suite_name, suite.name)

        #pin filter and assert that it turns orange
        suites_filter.pin_filter()
        Assert.equal(suites_filter.get_filter_color(), PINNED_FILTER_COLOR)

        #and check everything again on manage cases page
        manage_cases_pg.go_to_manage_cases_page()
        applied_filter = manage_cases_pg.filter_form.filter_items
        Assert.equal(len(applied_filter), 1)
        Assert.equal(applied_filter[0].content_text, good_case_name.lower())
        for case in manage_cases_pg.test_cases:
            Assert.contains(good_case_name, case.name)

        #and check everything one more time on manage suites page
        manage_suites_pg.go_to_manage_suites_page()
        applied_filter = manage_suites_pg.filter_form.filter_items
        Assert.equal(len(applied_filter), 1)
        Assert.equal(applied_filter[0].content_text, good_suite_name.lower())
        for suite in manage_suites_pg.test_suites:
            Assert.contains(good_suite_name, suite.name)

        #and go to manage runs page and see no filters there
        from pages.manage_runs_page import MozTrapManageRunsPage
        manage_runs_pg = MozTrapManageRunsPage(mozwebqa_logged_in)
        manage_runs_pg.go_to_manage_runs_page()

        #check that there is no filters applied
        Assert.equal(manage_runs_pg.filter_form.filter_items, [])
