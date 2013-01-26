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
        product_version = u'%s %s' % (product['name'], product['version']['name'])

        from pages.manage_runs_page import MozTrapManageRunsPage
        manage_runs_pg = MozTrapManageRunsPage(mozwebqa_logged_in)
        manage_runs_pg.go_to_manage_runs_page()
        manage_runs_pg.filter_runs_by_product_version(product_version)
        manage_runs_pg.pin_filter_by_product_version()

        Assert.equal(
            manage_runs_pg.get_pinned_filter_color(),
            PINNED_FILTER_COLOR,
            u'pinned filter\'s color is not orange')

        create_run_pg = manage_runs_pg.click_create_run_button()

        Assert.equal(
            create_run_pg.product_version_value,
            product_version,
            u'default product version is incorrect')

    @pytest.mark.moztrap(5936)
    @pytest.mark.nondestructive
    def test_that_pinning_filter_on_product_sets_defaults_in_new_product_version(self, mozwebqa_logged_in):
        product = self.create_product(mozwebqa_logged_in)

        from pages.manage_versions_page import MozTrapManageVersionsPage
        manage_versions_pg = MozTrapManageVersionsPage(mozwebqa_logged_in)
        manage_versions_pg.go_to_manage_versions_page()
        manage_versions_pg.filter_versions_by_product(product['name'])
        manage_versions_pg.pin_filter_by_product()

        Assert.equal(
            manage_versions_pg.get_pinned_filter_color(),
            PINNED_FILTER_COLOR,
            u'pinned filter\'s color is not orange')

        create_version_pg = manage_versions_pg.click_create_version_button()

        Assert.equal(
            create_version_pg.product_name_value,
            product['name'],
            u'default product is incorrect')
