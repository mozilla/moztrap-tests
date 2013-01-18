#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.color import Color

from pages.page import Page, PageRegion


class Filter(Page):

    _filter_input_locator = (By.ID, 'text-filter')
    _filter_suggestion_dropdown_locator = (By.CSS_SELECTOR, ".textual .suggest li a")
    _filter_suggestion_locator = (
        By.CSS_SELECTOR,
        '.textual .suggest .suggestion[data-type="%(filter_type)s"][data-name="%(filter_name)s"]')
    _filter_item_locator = (
        By.CSS_SELECTOR,
        'input[data-name="%(filter_type)s"][value="%(filter_name)s"]:checked + .onoff')

    def filter_by(self, lookup, value):
        _suggestion_locator = (
            self._filter_suggestion_locator[0],
            self._filter_suggestion_locator[1] % {'filter_type': lookup, 'filter_name': value})

        self.find_element(*self._filter_input_locator).send_keys(value)
        self.wait_for_element_to_be_visible(*_suggestion_locator)

        #find suggestion and get value of its data-id attribute
        suggestion = self.find_element(*_suggestion_locator)
        data_id = suggestion.get_attribute('data-id')
        suggestion.click()

        _filter_item_locator = (
            self._filter_item_locator[0],
            self._filter_item_locator[1] % {'filter_type': lookup, 'filter_name': data_id.lower()})

        self.wait_for_element_to_be_visible(*_filter_item_locator)
        self.wait_for_ajax()

        #find filter item and pass it as base element into FilterItem class
        filter_item = self.find_element(*_filter_item_locator)
        return FilterItem(self.testsetup, filter_item)

    def filter_without_mouse_by(self, lookup, value):
        filter_input = self.find_element(*self._filter_input_locator)
        filter_input.send_keys(value)

        self.wait_for_element_to_be_visible(*self._filter_suggestion_dropdown_locator)

        #find suggestion and get value of its data-id attribute
        suggestion = self.find_element(*self._filter_suggestion_dropdown_locator)
        data_id = suggestion.get_attribute('data-id')
        suggestion.click()

        _filter_item_locator = (
            self._filter_item_locator[0],
            self._filter_item_locator[1] % {'filter_type': lookup, 'filter_name': data_id.lower()})

        filter_input.send_keys(Keys.RETURN)
        self.wait_for_element_to_be_visible(*_filter_item_locator)
        self.wait_for_ajax()

        #find filter item and pass it as base element into FilterItem class
        filter_item = self.find_element(*_filter_item_locator)
        return FilterItem(self.testsetup, filter_item)


class FilterItem(PageRegion):

    _remove_button_locator = (By.CSS_SELECTOR, '.onoffswitch')
    _pin_button_locator = (By.CSS_SELECTOR, '.pinswitch')

    def pin_filter(self):
        self.find_element(*self._pin_button_locator).click()

    def remove_filter(self):
        self.find_element(*self._remove_button_locator).click()
        self.wait_for_ajax()

    def get_filter_color(self, coding='hex'):
        color = self._selenium_root.value_of_css_property('background-color')
        return getattr(Color.from_string(color), coding).upper()

    @property
    def is_pinned(self):
        return u'pinned' in self._selenium_root.get_attribute('className')
