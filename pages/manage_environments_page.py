#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import MozTrapBasePage


class MozTrapManageEnvironmentsPage(MozTrapBasePage):

    _page_title = 'Manage-Environments'

    _add_an_environment_link_locator = (By.CSS_SELECTOR, 'article.add-item h3')
    _elements_filter_input_locator = (By.ID, 'env-elements-input')
    _elements_suggestion_locator = (By.CSS_SELECTOR, 'a.suggestion[data-type="element"][data-name="%s"]')
    _added_elements_locator = (By.CSS_SELECTOR, '#add-environment-form ul.env-element-list')
    _save_environment_button_locator = (By.ID, 'add-environment')
    _environments_form_locator = (By.ID, 'productversion-environments-form')
    _done_editing_button_locator = (By.CSS_SELECTOR, 'div.form-actions a.done-link')

    def add_element_to_environment(self, element):
        self.wait_for_element_to_be_visible(*self._add_an_environment_link_locator)
        self.find_element(*self._add_an_environment_link_locator).click()
        self.wait_for_ajax()
        self.wait_for_element_to_be_visible(*self._elements_filter_input_locator)
        self.find_element(*self._elements_filter_input_locator).send_keys(element['name'])
        _elements_suggestion_locator = (
            self._elements_suggestion_locator[0],
            self._elements_suggestion_locator[1] % element['name']
        )
        self.wait_for_element_to_be_visible(*_elements_suggestion_locator)
        self.find_element(*_elements_suggestion_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: element['name'] in s.find_element(*self._added_elements_locator).text)
        self.find_element(*self._save_environment_button_locator).click()
        self.wait_for_ajax()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: element['name'] in s.find_element(*self._environments_form_locator).text)
        self.find_element(*self._done_editing_button_locator).click()
