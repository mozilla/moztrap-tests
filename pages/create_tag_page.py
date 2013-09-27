#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import MozTrapBasePage
from pages.regions.multiselect_widget import MultiselectWidget


class MozTrapCreateTagPage(MozTrapBasePage):

    _name_input_locator = (By.ID, 'id_name')
    _product_select_locator = (By.ID, 'id_product')
    _description_input_locator = (By.ID, 'id_description')
    _submit_button_locator = (By.CSS_SELECTOR, '.form-actions > button[type="submit"]')

    def create_tag(self, tag_mock, save_tag=True):
        self.find_element(*self._name_input_locator).send_keys(tag_mock.name)

        if tag_mock.product:
            product_select = Select(self.selenium.find_element(*self._product_select_locator))
            product_select.select_by_visible_text(tag_mock.product)

        self.find_element(*self._description_input_locator).send_keys(tag_mock.description)

        if save_tag:
            self.save_tag()

    def save_tag(self):
        self.find_element(*self._submit_button_locator).click()

    @property
    def multiselect_widget(self):
        return MultiselectWidget(self.testsetup)

    @property
    def is_multiselect_widget_visible(self):
        return self.multiselect_widget.is_visible

    @property
    def available_caseversions(self):
        return self.multiselect_widget.available_items

    def include_caseversions_to_tag(self, caseversions_list, save_tag=True):
        self.multiselect_widget.include_items(caseversions_list)
        if save_tag:
            self.save_tag()
