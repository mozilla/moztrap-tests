#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base_page import CaseConductorBasePage


class CaseConductorHomePage(CaseConductorBasePage):

    _page_title = 'Mozilla Case Conductor'
    _select_locator = u'css=.selectruns .finder .carousel .colcontent .title:contains(%(item_name)s)'
    _submit_locator = u'css=.drilldown .environment .form-actions button'

    def go_to_homepage_page(self):
        self.selenium.open('/')
        self.is_the_current_page

    def select_item(self, name):
        _select_locator = self._select_locator % {'item_name': name}

        self.click(_select_locator)
        self.wait_for_ajax()

    def go_to_run_test(self, product_name, cycle_name, run_name):
        self.select_item(product_name)
        self.select_item(cycle_name)
        self.select_item(run_name)
        self.click(self._submit_locator, wait_flag=True)
