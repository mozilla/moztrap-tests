#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.color import Color
from selenium.webdriver.common.keys import Keys

from pages.page import Page


class Filter(Page):

    _filter_input_locator = (By.ID, 'text-filter')
    _filter_suggestion_locator = (By.CSS_SELECTOR,
        '#filter .textual .suggest .suggestion[data-type="%(filter_type)s"][data-name="%(filter_name)s"]')
    _filter_suggestion_dropdown_locator = (By.CSS_SELECTOR, ".textual .suggest li a")
    _filter_remove_button_locator = (By.CSS_SELECTOR,
        '#filterform .filter-group input[data-name="%(filter_type)s"][value="%(filter_name)s"]:checked')
    _filter_pin_button_locator = (By.CSS_SELECTOR,
        '#filterform input[data-name="%(filter_type)s"]:checked + .onoff .pinswitch')
    _pinned_filter_locator = (By.CSS_SELECTOR, '#filterform .onoff.pinned')

    def remove_filter_by(self, lookup, value):
        _remove_button_locator = (
            self._filter_remove_button_locator[0],
            self._filter_remove_button_locator[1] % {'filter_type': lookup, 'filter_name': value.lower()})

        self.selenium.find_element(*_remove_button_locator).click()
        self.wait_for_ajax()

    def filter_by(self, lookup, value):
        _suggestion_locator = (
            self._filter_suggestion_locator[0],
            self._filter_suggestion_locator[1] % {'filter_type': lookup, 'filter_name': value})

        self.selenium.find_element(*self._filter_input_locator).send_keys(value)
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: self.is_element_visible(*_suggestion_locator),
            u'expected filter suggestion is not visible')
        self.selenium.find_element(*_suggestion_locator).click()
        self.wait_for_ajax()

    def filter_by_without_mouse(self, lookup, value):
        #_suggestion_locator = (
        #    self._filter_suggestion_locator[0],
        #    self._filter_suggestion_locator[1] % {'filter_type': lookup, 'filter_name': value})

        filter_input  = self.selenium.find_element(*self._filter_input_locator)
        filter_input.send_keys(value)

        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: self.is_element_visible(*self._filter_suggestion_dropdown_locator),
            u'expected filter suggestion is not visible')
        filter_input.send_keys(Keys.RETURN)
        self.wait_for_ajax()

    def pin_filter(self, lookup):
        _pin_button_locator = (
            self._filter_pin_button_locator[0],
            self._filter_pin_button_locator[1] % {'filter_type': lookup})
        self.selenium.find_element(*_pin_button_locator).click()

    @property
    def pinned_filter_color(self, coding='hex'):
        pinned_filter = self.selenium.find_element(*self._pinned_filter_locator)
        color = pinned_filter.value_of_css_property('background-color')
        return getattr(Color.from_string(color), coding)
