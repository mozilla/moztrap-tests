#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base_page import MozTrapBasePage
from pages.regions.filter import Filter


class MozTrapManageSuitesPage(MozTrapBasePage):

    _page_title = 'Manage-Suites'

    _delete_suite_locator = (By.CSS_SELECTOR, '#managesuites .itemlist .listitem[data-title="%(suite_name)s"] .action-delete')
    _suite_status_locator = (By.CSS_SELECTOR, '#managesuites .itemlist .listitem[data-title="%(suite_name)s"] .status-action')
    _view_cases_locator = ((By.CSS_SELECTOR, '#managesuites .itemlist .listitem[data-title="%(suite_name)s"] .casecount .drill-link'))

    @property
    def filter_form(self):
        return Filter(self.testsetup)

    def go_to_manage_suites_page(self):
        self.selenium.get(self.base_url + '/manage/suites/')
        self.is_the_current_page

    def delete_suite(self, name='Test Suite'):
        _delete_locator = (self._delete_suite_locator[0], self._delete_suite_locator[1] % {'suite_name': name})

        self.selenium.find_element(*_delete_locator).click()
        self.wait_for_ajax()

    def activate_suite(self, name='Test Suite'):
        _suite_status_locator = (self._suite_status_locator[0], self._suite_status_locator[1] % {'suite_name': name})

        self.selenium.find_element(*self._suite_status_locator).click()
        self.wait_for_ajax()

    def view_cases(self, name='Test Suite'):
        _view_cases_locator = (self._view_cases_locator[0], self._view_cases_locator[1] % {'suite_name': name})
        self.selenium.find_element(*_view_cases_locator).click()
        from pages.manage_cases_page import MozTrapManageCasesPage
        return MozTrapManageCasesPage(self.testsetup)
