#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base_page import CaseConductorBasePage


class CaseConductorManageProductsPage(CaseConductorBasePage):

    _page_title = "Mozilla Case Conductor"
    _delete_product_locator = u"css=#manageproducts article.item .title:contains(%(product_name)s) ~ .controls button[title='delete']"
    _input_locator = 'id=text-filter'
    _update_list_locator = 'css=#filter .visual .content .form-actions button'
    _filter_suggestion_locator = u'css=#filter .textual .suggest a:contains(%(filter_name)s)'
    _filter_locator = u'css=#filter .visual .filter-group input[value="%(filter_name)s"]'

    def go_to_manage_products_page(self):
        self.selenium.open('/manage/products/')
        self.is_the_current_page

    def delete_product(self, name="Test Product"):
        _delete_locator = self._delete_product_locator % {"product_name": name}

        self.click(_delete_locator)
        self.wait_for_ajax()

    def filter_products_by_name(self, name):
        _filter_suggestion_locator = self._filter_suggestion_locator % {'filter_name': name}
        _name_without_last_character = name[:-1]
        _name_last_character = name[-1]

        self.type(self._input_locator, _name_without_last_character)
        self.key_pressed(self._input_locator, _name_last_character)
        self.wait_for_element_present(_filter_suggestion_locator)
        self.click(_filter_suggestion_locator)
        self.wait_for_element_visible(self._update_list_locator)
        self.click(self._update_list_locator, wait_flag=True)

    def filter_products_by_name_without_mouse(self, name):
        _filter_suggestion_locator = self._filter_suggestion_locator % {'filter_name': name}
        _name_without_last_character = name[:-1]
        _name_last_character = name[-1]

        self.type(self._input_locator, _name_without_last_character)
        self.key_pressed(self._input_locator, _name_last_character)
        self.wait_for_element_present(_filter_suggestion_locator)
        self.key_pressed(self._input_locator, '\\13')
        self.wait_for_element_visible(self._update_list_locator)
        self.key_pressed(self._input_locator, '\\13')
        self.selenium.wait_for_page_to_load(self.timeout)

    def remove_name_filter(self, name):
        _filter_locator = self._filter_locator % {'filter_name': name.lower()}

        self.click(_filter_locator)
        self.wait_for_element_visible(self._update_list_locator)
        self.click(self._update_list_locator, wait_flag=True)
