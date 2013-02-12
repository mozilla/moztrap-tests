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
    def test_that_pinning_filter_on_product_version_set_defaults_in_new_run(self, mozwebqa_logged_in):
        product = self.create_product(mozwebqa_logged_in)
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

    @pytest.mark.moztrap(5933)
    @pytest.mark.nondestructive
    def test_that_pinning_filters_on_product_sets_defaults_in_new_suite(self, mozwebqa_logged_in):
        product = self.create_product(mozwebqa_logged_in)

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

    @pytest.mark.moztrap(5936)
    @pytest.mark.nondestructive
    def test_that_pinning_filter_on_product_sets_defaults_in_new_product_version(self, mozwebqa_logged_in):
        product = self.create_product(mozwebqa_logged_in)

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
