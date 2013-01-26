#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.color import Color

from pages.base_page import MozTrapBasePage


class MozTrapManageVersionsPage(MozTrapBasePage):

    _page_title = 'Manage-Versions'

    _version_manage_locator = (By.CSS_SELECTOR, '#manageproductversions .listitem .title[title="%(product_name)s %(version_name)s"]')
    _version_homepage_locator = (By.CSS_SELECTOR, '.runsdrill .runsfinder .productversions .colcontent .title[title="%(version_name)s"][data-product="%(product_name)s"])')
    _create_version_button_locator = (By.CSS_SELECTOR, '#manageproductversions .create.single')
    _delete_version_locator = (By.CSS_SELECTOR, '#manageproductversions .listitem .action-delete[title="delete %(product_name)s %(version_name)s"]')
    _clone_version_locator = (By.CSS_SELECTOR, '#manageproductversions .listitem .action-clone[title="clone %(product_name)s %(version_name)s"]')
    _filter_input_locator = (By.ID, 'text-filter')
    _filter_suggestion_locator = (By.CSS_SELECTOR, '#filter .suggestion[data-type="%(filter_lookup)s"][data-name="%(filter_name)s"]')
    _filter_locator = (By.CSS_SELECTOR, '#filterform input[data-name="%(filter_lookup)s"][value="%(filter_name)s"]:checked + span label')
    _pin_filter_button_locator = (By.CSS_SELECTOR, '#filterform input[data-name="%(filter_lookup)s"]:checked + .onoff .pinswitch')
    _pinned_filter_locator = (By.CSS_SELECTOR, '#filterform .onoff.pinned')

    def go_to_manage_versions_page(self):
        self.get_relative_path('/manage/productversions/')
        self.is_the_current_page

    def click_create_version_button(self):
        self.selenium.find_element(*self._create_version_button_locator).click()
        from pages.create_version_page import MozTrapCreateVersionPage
        return MozTrapCreateVersionPage(self.testsetup)

    def delete_version(self, name='Test Version', product_name='Test Product'):
        _delete_locator = (self._delete_version_locator[0], self._delete_version_locator[1] % {'product_name': product_name, 'version_name': name})

        self.selenium.find_element(*_delete_locator).click()
        self.wait_for_ajax()

    def filter_versions_by_name(self, name):
        _filter_locator = (
            self._filter_locator[0],
            self._filter_locator[1] % {'filter_lookup': 'version', 'filter_name': name.lower()})
        _filter_suggestion_locator = (
            self._filter_suggestion_locator[0],
            self._filter_suggestion_locator[1] % {'filter_lookup': 'version', 'filter_name': name})

        self.selenium.find_element(*self._filter_input_locator).send_keys(name)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*_filter_suggestion_locator))
        self.selenium.find_element(*_filter_suggestion_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*_filter_locator))
        self.wait_for_ajax()

    def filter_versions_by_product(self, product_name):
        _filter_suggestion_locator = (
            self._filter_suggestion_locator[0],
            self._filter_suggestion_locator[1] % {'filter_lookup': 'product', 'filter_name': product_name})

        self.selenium.find_element(*self._filter_input_locator).send_keys(product_name)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*_filter_suggestion_locator))

        suggestion = self.selenium.find_element(*_filter_suggestion_locator)
        data_id = suggestion.get_attribute('data-id')
        suggestion.click()

        _filter_locator = (
            self._filter_locator[0],
            self._filter_locator[1] % {'filter_lookup': 'product', 'filter_name': data_id.lower()})

        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*_filter_locator))
        self.wait_for_ajax()

    def remove_name_filter(self, name):
        _filter_locator = (self._filter_locator[0], self._filter_locator[1] % {'filter_name': name.lower()})

        self.selenium.find_element(*_filter_locator).click()
        self.wait_for_ajax()

    def clone_version(self, name='Test Version', product_name='Test Product'):
        _clone_version_locator = (self._clone_version_locator[0], self._clone_version_locator[1] % {'product_name': product_name, 'version_name': name})
        cloned_version = {}

        self.selenium.find_element(*_clone_version_locator).click()
        self.wait_for_ajax()

        cloned_version['product_name'] = product_name
        cloned_version['name'] = name + '.next'
        cloned_version['manage_locator'] = (self._version_manage_locator[0], self._version_manage_locator[1] % {'product_name': cloned_version['product_name'], 'version_name': cloned_version['name']})
        cloned_version['homepage_locator'] = (self._version_homepage_locator[0], self._version_homepage_locator[1] % {'product_name': cloned_version['product_name'], 'version_name': cloned_version['name']})

        return cloned_version

    def pin_filter_by_product(self):
        _pin_filter_button_locator = (
            self._pin_filter_button_locator[0],
            self._pin_filter_button_locator[1] % {'filter_lookup': 'product'})
        self.selenium.find_element(*_pin_filter_button_locator).click()

    def get_pinned_filter_color(self, coding='hex'):
        pinned_filter = self.selenium.find_element(*self._pinned_filter_locator)
        color = pinned_filter.value_of_css_property('background-color')
        return getattr(Color.from_string(color), coding).upper()
