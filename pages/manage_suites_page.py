#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base_page import MozTrapBasePage


class MozTrapManageSuitesPage(MozTrapBasePage):

    _page_title = 'MozTrap'

    _delete_suite_locator = (By.CSS_SELECTOR, '#managesuites .itemlist .listitem[data-title="%(suite_name)s"] .action-delete')
    _suite_status_locator = (By.CSS_SELECTOR, '#managesuites .itemlist .listitem[data-title="%(suite_name)s"] .status-action')
    _filter_input_locator = (By.ID, 'text-filter')
    _filter_suggestion_locator = (By.CSS_SELECTOR, '#filter .textual .suggest .suggestion[data-type="name"][data-name="%(filter_name)s"]')
    _filter_locator = (By.CSS_SELECTOR, '#filterform .filter-group input[data-name="name"][value="%(filter_name)s"]:checked')

    def go_to_manage_suites_page(self):
        self.selenium.get(self.base_url + '/manage/suites/')
        self.is_the_current_page

    def delete_suite(self, name='Test Suite'):
        _delete_locator = (self._delete_suite_locator[0], self._delete_suite_locator[1] % {'suite_name': name})

        self.selenium.find_element(*_delete_locator).click()
        self.wait_for_ajax()

    def filter_suites_by_name(self, name):
        _filter_suggestion_locator = (self._filter_suggestion_locator[0], self._filter_suggestion_locator[1] % {'filter_name': name})

        self.selenium.find_element(*self._filter_input_locator).send_keys(name)
        self.selenium.find_element(*_filter_suggestion_locator).click()
        self.wait_for_ajax()

    def activate_suite(self, name='Test Suite'):
        _suite_status_locator = (self._suite_status_locator[0], self._suite_status_locator[1] % {'suite_name': name})

        self.selenium.find_element(*self._suite_status_locator).click()
        self.wait_for_ajax()
