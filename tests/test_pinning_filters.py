#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert

from pages.base_test import BaseTest
from pages.manage_runs_page import MozTrapManageRunsPage


class TestPinningFilters(BaseTest):

    @pytest.mark.moztrap(5935)
    @pytest.mark.nondestructive
    def test_that_pinning_filter_on_product_version_set_defaults_in_new_run(self, mozwebqa_logged_in):
        pinned_filter_color = u'#DFB081'
        product = self.create_product(mozwebqa_logged_in)
        product_version_name = u'%s %s' % (product['name'], product['version']['name'])

        manage_runs_pg = MozTrapManageRunsPage(mozwebqa_logged_in)
        manage_runs_pg.go_to_manage_runs_page()
        filter_item = manage_runs_pg.filter_form.filter_by(
                lookup='productversion',
                value=product_version_name)

        #check that filter is not orange before it's pinned
        Assert.not_equal(
            filter_item.get_filter_color(),
            pinned_filter_color)

        filter_item.pin_filter()

        #check that filter is orange after it's been pinned
        Assert.equal(
            filter_item.get_filter_color(),
            pinned_filter_color)

        create_run_pg = manage_runs_pg.click_create_run_button()

        Assert.equal(
            create_run_pg.product_version,
            product_version_name)
