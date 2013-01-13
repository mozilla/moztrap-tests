#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color

from pages.base_page import MozTrapBasePage


class MozTrapManageRunsPage(MozTrapBasePage):

    _page_title = 'Manage-Runs'

    _delete_run_locator = (By.CSS_SELECTOR, '#manageruns .itemlist .listitem[data-title="%(run_name)s"] .action-delete')
    _run_activate_locator = (By.CSS_SELECTOR, '#manageruns .itemlist .listitem[data-title="%(run_name)s"] .status-action.active')
    _run_status_locator = (By.CSS_SELECTOR, '#manageruns .itemlist .listitem[data-title="%(run_name)s"] .status-title')
    _filter_input_locator = (By.ID, 'text-filter')
    _filter_suggestion_by_name_locator = (By.CSS_SELECTOR,
        '#filter .textual .suggest .suggestion[data-type="name"][data-name="%(filter_name)s"]')
    _filter_suggestion_by_product_version_locator = (By.CSS_SELECTOR,
        '#filter .textual .suggest .suggestion[data-type="productversion"][data-name="%(filter_name)s"]')
    _filter_locator = (By.CSS_SELECTOR,
        '#filterform .filter-group input[data-name="name"][value="%(filter_name)s"]:checked')
    _pin_filter_button_locator = (By.CSS_SELECTOR,
        '#filterform input[data-name="productversion"]:checked + .onoff .pinswitch')
    _pinned_filter_locator = (By.CSS_SELECTOR, '#filterform .onoff.pinned')

    def go_to_manage_runs_page(self):
        self.selenium.get(self.base_url + '/manage/runs/')
        self.is_the_current_page

    def delete_run(self, name='Test Run'):
        _delete_locator = (self._delete_run_locator[0], self._delete_run_locator[1] % {'run_name': name})

        self.selenium.find_element(*_delete_locator).click()
        self.wait_for_ajax()

    def filter_runs_by_name(self, name):
        _filter_suggestion_locator = (
            self._filter_suggestion_by_name_locator[0],
            self._filter_suggestion_by_name_locator[1] % {'filter_name': name})

        self.selenium.find_element(*self._filter_input_locator).send_keys(name)
        self.selenium.find_element(*_filter_suggestion_locator).click()
        self.wait_for_ajax()

    def filter_runs_by_product_version(self, product_version):
        _filter_suggestion_locator = (
            self._filter_suggestion_by_product_version_locator[0],
            self._filter_suggestion_by_product_version_locator[1] % {'filter_name': product_version})

        self.selenium.find_element(*self._filter_input_locator).send_keys(product_version)
        self.selenium.find_element(*_filter_suggestion_locator).click()
        self.wait_for_ajax()

    def remove_name_filter(self, name):
        _filter_locator = (self._filter_locator[0], self._filter_locator[1] % {'filter_name': name.lower()})

        self.selenium.find_element(*self._filter_locator).click()
        self.wait_for_ajax()

    def activate_run(self, name='Test Run'):
        _run_activate_locator = (self._run_activate_locator[0], self._run_activate_locator[1] % {'run_name': name})
        _run_status_locator = (self._run_status_locator[0], self._run_status_locator[1] % {'run_name': name})

        self.selenium.find_element(*_run_status_locator).click()
        self.selenium.find_element(*_run_activate_locator).click()

        self.wait_for_ajax()

    def pin_product_version(self):
        self.selenium.find_element(*self._pin_filter_button_locator).click()

    @property
    def pinned_filter_color(self, coding='hex'):
        pinned_filter = self.selenium.find_element(*self._pinned_filter_locator)
        color = pinned_filter.value_of_css_property('background-color')
        return getattr(Color.from_string(color), coding)
