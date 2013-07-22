#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base_page import MozTrapBasePage


class MozTrapCreateTagPage(MozTrapBasePage):

    _name_input_locator = (By.ID, 'id_name')
    _description_input_locator = (By.ID, 'id_description')
    _submit_button_locator = (By.CSS_SELECTOR, '.form-actions > button[type="submit"]')
    _multiselect_widget_locator = (By.CSS_SELECTOR, '.multiselect')

    def create_tag(self, tag_mock):
        self.find_element(*self._name_input_locator).send_keys(tag_mock.name)
        self.find_element(*self._description_input_locator).send_keys(tag_mock.description)
        self.find_element(*self._submit_button_locator).click()

    @property
    def is_multiselect_widget_visible(self):
        return self.is_element_visible(*self._multiselect_widget_locator)
