#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base_page import MozTrapBasePage


class MozTrapManageProductsPage(MozTrapBasePage):

    _page_title = 'MozTrap'
    _delete_product_locator = u'css=#manageproducts .listitem .controls .action-delete[title="delete %(product_name)s"]'
    _filter_input_locator = 'id=text-filter'
    _filter_suggestion_locator = u'css=#filter .textual .suggest .suggestion[data-type="name"][data-name="%(filter_name)s"]'
    _filter_locator = u'css=#filterform .filter-group input[data-name="name"][value="%(filter_name)s"]:checked'

    def go_to_manage_products_page(self):
        self.selenium.open('/manage/products/')
        self.is_the_current_page

    def delete_product(self, name='Test Product'):
        _delete_locator = self._delete_product_locator % {'product_name': name}

        self.click(_delete_locator)
        self.wait_for_ajax()

    def filter_products_by_name(self, name):
        _filter_locator = self._filter_locator % {'filter_name': name.lower()}
        _filter_suggestion_locator = self._filter_suggestion_locator % {'filter_name': name}

        self.type(self._filter_input_locator, name)
        self.selenium.type_keys(self._filter_input_locator, name)
        self.wait_for_element_present(_filter_suggestion_locator)
        self.click(_filter_suggestion_locator)
        self.wait_for_element_present(_filter_locator)
        self.wait_for_ajax()

    def filter_products_by_name_without_mouse(self, name):
        _filter_locator = self._filter_locator % {'filter_name': name.lower()}
        _filter_suggestion_locator = self._filter_suggestion_locator % {'filter_name': name}

        self.type(self._filter_input_locator, name)
        self.selenium.type_keys(self._filter_input_locator, name)
        self.wait_for_element_present(_filter_suggestion_locator)
        self.selenium.key_down(self._filter_input_locator, '13')
        self.wait_for_element_present(_filter_locator)
        self.wait_for_ajax()

    def remove_name_filter(self, name):
        _filter_locator = self._filter_locator % {'filter_name': name.lower()}

        self.click(_filter_locator)
        self.wait_for_ajax()
