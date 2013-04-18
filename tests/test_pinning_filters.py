#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.base_test import BaseTest


PINNED_FILTER_COLOR = u'#DFB081'


class TestPinningFilters(BaseTest):

    @pytest.mark.moztrap(5935)
    @pytest.mark.nondestructive
    def test_that_pinning_filter_on_product_version_set_defaults_in_new_run(self, mozwebqa_logged_in, product):
        product_version_name = u'%s %s' % (product['name'], product['version']['name'])

        from pages.manage_runs_page import MozTrapManageRunsPage
        manage_runs_pg = MozTrapManageRunsPage(mozwebqa_logged_in)
        manage_runs_pg.go_to_manage_runs_page()
        filter_item = manage_runs_pg.filter_form.filter_by(lookup='productversion', value=product_version_name)

        #check that filter is not orange before it's pinned
        Assert.not_equal(
            filter_item.get_filter_color(),
            PINNED_FILTER_COLOR,
            u'filter is orange before it was pinned')

        filter_item.pin_filter()

        #check that filter is orange after it's been pinned
        Assert.equal(
            filter_item.get_filter_color(),
            PINNED_FILTER_COLOR,
            u'pinned filter\'s color is not orange')

        create_run_pg = manage_runs_pg.click_create_run_button()

        Assert.equal(
            create_run_pg.product_version_value,
            product_version_name,
            u'default product version is incorrect')

    @pytest.mark.moztrap(5930)
    @pytest.mark.nondestructive
    def test_that_pinning_name_field_filter_only_works_for_current_page(self, mozwebqa_logged_in, product):
        good_case_name = u'MOZILLA'
        good_suite_name = u'MozTrap'

        self.create_bulk_cases(mozwebqa_logged_in, name=good_case_name, product=product, cases_amount=3)
        self.create_bulk_cases(mozwebqa_logged_in, name=u'ALLIZOM', product=product, cases_amount=2)
        self.create_suite(mozwebqa_logged_in, name=good_suite_name, product=product, use_API=True)
        self.create_suite(mozwebqa_logged_in, name=u'PartZom', product=product, use_API=True)

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

    @pytest.mark.moztrap(5933)
    @pytest.mark.nondestructive
    def test_that_pinning_filters_on_product_sets_defaults_in_new_suite(self, mozwebqa_logged_in, product):
        from pages.manage_suites_page import MozTrapManageSuitesPage
        manage_suites_pg = MozTrapManageSuitesPage(mozwebqa_logged_in)
        manage_suites_pg.go_to_manage_suites_page()
        filter_item = manage_suites_pg.filter_form.filter_by(lookup='product', value=product['name'])

        #check that filter is not orange before it's pinned
        Assert.not_equal(
            filter_item.get_filter_color(),
            PINNED_FILTER_COLOR,
            u'filter is orange before it was pinned')

        filter_item.pin_filter()

        #check that filter is orange after it's been pinned
        Assert.equal(
            filter_item.get_filter_color(),
            PINNED_FILTER_COLOR,
            u'pinned filter\'s color is not orange')

        create_suite_pg = manage_suites_pg.click_create_suite_button()

        Assert.equal(
            create_suite_pg.product_name_value,
            product['name'],
            u'default product is incorrect')

    @pytest.mark.moztrap(5932)
    @pytest.mark.nondestructive
    def test_that_pinning_filters_on_product_and_version_and_suite_set_defaults_in_new_case(self, mozwebqa_logged_in, product):
        version = product['version']
        product_version_name = u'%s %s' % (product['name'], version['name'])
        suite = self.create_suite(mozwebqa_logged_in, product=product, use_API=True)

        from pages.manage_cases_page import MozTrapManageCasesPage
        manage_cases_pg = MozTrapManageCasesPage(mozwebqa_logged_in)
        manage_cases_pg.go_to_manage_cases_page()

        filters = []
        filters.append(manage_cases_pg.filter_form.filter_by(lookup='product', value=product['name']))
        filters.append(manage_cases_pg.filter_form.filter_by(lookup='productversion', value=product_version_name))
        filters.append(manage_cases_pg.filter_form.filter_by(lookup='suite', value=suite['name']))

        for item in filters:
            item.pin_filter()
            Assert.equal(item.get_filter_color(), PINNED_FILTER_COLOR)

        #go to create case page
        create_case_pg = manage_cases_pg.click_create_case_button()
        Assert.equal(create_case_pg.product_value, product['name'])
        Assert.equal(create_case_pg.product_version_value, version['name'])
        Assert.equal(create_case_pg.suite_value, suite['name'])

        create_case_pg.go_back()

        #go to create bulk cases page
        create_bulk_cases_pg = manage_cases_pg.click_create_bulk_cases_button()
        Assert.equal(create_bulk_cases_pg.product_value, product['name'])
        Assert.equal(create_bulk_cases_pg.product_version_value, version['name'])
        Assert.equal(create_bulk_cases_pg.suite_value, suite['name'])

    @pytest.mark.moztrap(5936)
    @pytest.mark.nondestructive
    def test_that_pinning_filter_on_product_sets_defaults_in_new_product_version(self, mozwebqa_logged_in, product):
        from pages.manage_versions_page import MozTrapManageVersionsPage
        manage_versions_pg = MozTrapManageVersionsPage(mozwebqa_logged_in)
        manage_versions_pg.go_to_manage_versions_page()
        filter_item = manage_versions_pg.filter_form.filter_by(lookup='product', value=product['name'])

        #check that filter is not orange before it's pinned
        Assert.not_equal(
            filter_item.get_filter_color(),
            PINNED_FILTER_COLOR,
            u'filter is orange before it was pinned')

        filter_item.pin_filter()

        #check that filter is orange after it's been pinned
        Assert.equal(
            filter_item.get_filter_color(),
            PINNED_FILTER_COLOR,
            u'pinned filter\'s color is not orange')

        create_version_pg = manage_versions_pg.click_create_version_button()

        Assert.equal(
            create_version_pg.product_name_value,
            product['name'],
            u'default product is incorrect')
