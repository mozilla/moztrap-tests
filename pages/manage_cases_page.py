#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import PageRegion
from pages.base_page import MozTrapBasePage
from pages.regions.filter import Filter


class MozTrapManageCasesPage(MozTrapBasePage):

    _page_title = 'Manage-Cases'

    _test_case_item_locator = (By.CSS_SELECTOR, '.listitem.active')
    _create_case_button_locator = (By.CSS_SELECTOR, '#managecases .create.single')
    _create_bulk_cases_button_locator = (By.CSS_SELECTOR, '#managecases .create.bulk')

    @property
    def filter_form(self):
        return Filter(self.testsetup)

    def go_to_manage_cases_page(self):
        self.selenium.get(self.base_url + '/manage/cases/')
        self.is_the_current_page

    def click_create_case_button(self):
        self.find_element(*self._create_case_button_locator).click()
        from pages.create_case_page import MozTrapCreateCasePage
        return MozTrapCreateCasePage(self.testsetup)

    def click_create_bulk_cases_button(self):
        self.find_element(*self._create_bulk_cases_button_locator).click()
        from pages.create_bulk_cases_page import MozTrapCreateBulkCasesPage
        return MozTrapCreateBulkCasesPage(self.testsetup)

    def delete_case(self, name='Test Case'):
        self._get_case(name).delete()

    def _get_case(self, name):
        for case in self.test_cases:
            if case.name == name:
                return case
        raise NameError('test case with %s name not found' % name)

    @property
    def test_cases(self):
        return [self.TestCaseItem(self.testsetup, web_element)
                for web_element in self.find_elements(*self._test_case_item_locator)]

    class TestCaseItem(PageRegion):

        _case_product_version_locator = (By.CSS_SELECTOR, '.product')
        _case_name_locator = (By.CSS_SELECTOR, '.title')
        _delete_case_locator = (By.CSS_SELECTOR, '.action-delete')

        @property
        def name(self):
            return self.find_element(*self._case_name_locator).text

        @property
        def product_version(self):
            return self.find_element(*self._case_product_version_locator).text

        def delete(self):
            self.find_element(*self._delete_case_locator).click()
            self.wait_for_ajax()
