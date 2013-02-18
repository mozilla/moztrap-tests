#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base_page import MozTrapBasePage
from pages.regions.filter import Filter
from pages.page import PageRegion


class MozTrapManageRunsPage(MozTrapBasePage):

    _page_title = 'Manage-Runs'

    _create_run_button_locator = (By.CSS_SELECTOR, '#manageruns .create.single')
    _test_run_item_locator = (By.CSS_SELECTOR, '#manage-runs-form .listitem')

    @property
    def filter_form(self):
        return Filter(self.testsetup)

    @property
    def test_runs(self):
        return [self.TestRunItem(self.testsetup, web_element)
                for web_element in self.find_elements(*self._test_run_item_locator)]

    def go_to_manage_runs_page(self):
        self.selenium.get(self.base_url + '/manage/runs/')
        self.is_the_current_page

    def click_create_run_button(self):
        self.find_element(*self._create_run_button_locator).click()
        from pages.create_run_page import MozTrapCreateRunPage
        return MozTrapCreateRunPage(self.testsetup)

    def delete_run(self, name='Test Run'):
        self._get_run(name).delete()

    def activate_run(self, name='Test Run'):
        self._get_run(name).activate()

    def make_run_draft(self, name='Test Run'):
        self._get_run(name).make_draft()

    def go_to_edit_run_page(self, name='Test Run'):
        return self._get_run(name).edit()

    def _get_run(self, name):
        for run in self.test_runs:
            if run.name == name:
                return run
        raise NameError(u'test run with %s name not found' % name)

    class TestRunItem(PageRegion):

        _run_title_locator = (By.CSS_SELECTOR, '.title')
        _delete_run_locator = (By.CSS_SELECTOR, '.action-delete')
        _edit_run_locator = (By.CSS_SELECTOR, '.edit-link')
        _run_status_locator = (By.CSS_SELECTOR, '.status-title')
        _run_status_options_locator = (By.CSS_SELECTOR, '.status-options')
        _run_activate_locator = (By.CSS_SELECTOR, '.status-action.active')
        _run_draft_locator = (By.CSS_SELECTOR, '.status-action.draft')
        _run_show_details_locator = (By.CSS_SELECTOR, '.summary.item-summary')
        _run_expanded_content_locator = (By.CSS_SELECTOR, '.content.item-content.loaded')
        _included_suite_item_locator = (By.CSS_SELECTOR, '.suites .suite-list .suite')

        @property
        def name(self):
            return self.find_element(*self._run_title_locator).text

        def delete(self):
            self.find_element(*self._delete_run_locator).click()
            self.wait_for_ajax()

        def edit(self):
            self.selenium.find_element(*self._edit_run_locator).click()
            from pages.edit_run_page import MozTrapEditRunPage
            return MozTrapEditRunPage(self.testsetup)

        def activate(self):
            self.find_element(*self._run_status_locator).click()
            self.wait_for_element_to_be_visible(*self._run_status_options_locator)
            self.find_element(*self._run_activate_locator).click()
            self.wait_for_ajax()

        def make_draft(self):
            self.find_element(*self._run_status_locator).click()
            self.wait_for_element_to_be_visible(*self._run_status_options_locator)
            self.find_element(*self._run_draft_locator).click()
            self.wait_for_ajax()

        def show_details(self):
            self.find_element(*self._run_show_details_locator).click()
            self.wait_for_element_to_be_visible(*self._run_expanded_content_locator)

        @property
        def included_suites(self):
            return [item.text for item in self.find_elements(*self._included_suite_item_locator)]
