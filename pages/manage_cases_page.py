#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import MozTrapBasePage


class MozTrapManageCasesPage(MozTrapBasePage):

    _page_title = 'MozTrap'

    _delete_case_locator = (By.CSS_SELECTOR, '#managecases .itemlist .listitem[data-title="%(case_name)s"] .action-delete')
    _case_status_locator = (By.CSS_SELECTOR, '#managecases .itemlist .listitem[data-title="%(case_name)s"] .status-action')
    _filter_input_locator = (By.ID, 'text-filter')
    _filter_suggestion_locator = (By.CSS_SELECTOR, '#filter .textual .suggest .suggestion[data-type="name"][data-name="%(filter_name)s"]')
    _filter_locator = (By.CSS_SELECTOR, '#filterform .filter-group input[data-name="name"][value="%(filter_name)s"]:checked')

    def go_to_manage_cases_page(self):
        self.selenium.get(self.base_url + '/manage/cases/')
        self.is_the_current_page

    def delete_case(self, name='Test Case'):
        find_element(*self._delect_case_locator).click()

    def filter_cases_by_name(self, name):
        self.selenium.find_element(*self._filter_locator % {'filter_name': name.lower()})
        self.selenium.find_element(*self._filter_suggestion_locator % {'filter_name': name})

        name_field = self.selenium.find_element(*self._filter_input_locator)
        name_field.send_keys(name)

        self.selenium.find_element(*self._filter_suggestion_locator).click()

    def activate_case(self, name='Test Case'):
        find_element(*self._case_status_locator).click()
