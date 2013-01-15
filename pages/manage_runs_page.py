#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base_page import MozTrapBasePage
from pages.regions.filter import Filter


class MozTrapManageRunsPage(MozTrapBasePage):

    _page_title = 'Manage-Runs'

    _create_run_locator = (By.CSS_SELECTOR, '#manageruns .create.single')
    _delete_run_locator = (By.CSS_SELECTOR, '#manageruns .itemlist .listitem[data-title="%(run_name)s"] .action-delete')
    _run_activate_locator = (By.CSS_SELECTOR, '#manageruns .itemlist .listitem[data-title="%(run_name)s"] .status-action.active')
    _run_status_locator = (By.CSS_SELECTOR, '#manageruns .itemlist .listitem[data-title="%(run_name)s"] .status-title')

    @property
    def filter_form(self):
        return Filter(self.testsetup)

    def go_to_manage_runs_page(self):
        self.selenium.get(self.base_url + '/manage/runs/')
        self.is_the_current_page

    def click_create_run_button(self):
        self.selenium.find_element(*self._create_run_locator).click()
        from pages.create_run_page import MozTrapCreateRunPage
        return MozTrapCreateRunPage(self.testsetup)

    def delete_run(self, name='Test Run'):
        _delete_locator = (self._delete_run_locator[0], self._delete_run_locator[1] % {'run_name': name})

        self.selenium.find_element(*_delete_locator).click()
        self.wait_for_ajax()

    def activate_run(self, name='Test Run'):
        _run_activate_locator = (self._run_activate_locator[0], self._run_activate_locator[1] % {'run_name': name})
        _run_status_locator = (self._run_status_locator[0], self._run_status_locator[1] % {'run_name': name})

        self.selenium.find_element(*_run_status_locator).click()
        self.selenium.find_element(*_run_activate_locator).click()

        self.wait_for_ajax()
