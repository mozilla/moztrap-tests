#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.page import PageRegion
from pages.base_page import MozTrapBasePage


class MozTrapManageCasesPage(MozTrapBasePage):

    _page_title = 'Manage-Cases'

    _case_status_locator = (By.CSS_SELECTOR, '#managecases .itemlist .listitem[data-title="%(case_name)s"] .status-action')
    _filter_input_locator = (By.ID, 'text-filter')
    _filter_suggestion_locator = (By.CSS_SELECTOR, '#filter .suggestion[data-type="%(filter_lookup)s"][data-name="%(filter_name)s"]')
    _test_case_item_locator = (By.CSS_SELECTOR, '.listitem.active')

    def go_to_manage_cases_page(self):
        self.selenium.get(self.base_url + '/manage/cases/')
        self.is_the_current_page

    def delete_case(self, lookup='name', value='Test Case'):
        for case in self.test_cases:
            if getattr(case, lookup.replace(u' ', u'_')) == value:
                case.delete()
                break
        self.wait_for_ajax()

    def filter_cases(self, lookup, value):
        '''
        Types the name into the input field and then clicks the item in the search suggestions
        '''
        _filter_suggestion_locator = (
            self._filter_suggestion_locator[0],
            self._filter_suggestion_locator[1] % {'filter_lookup': lookup, 'filter_name': value})

        self.selenium.find_element(*self._filter_input_locator).send_keys(value)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*_filter_suggestion_locator))
        self.selenium.find_element(*_filter_suggestion_locator).click()
        self.wait_for_ajax()

    def activate_case(self, name='Test Case'):
        _case_status_locator = (self._case_status_locator[0], self._case_status_locator[1] % {'case_name': name})

        self.selenium.find_element(*_case_status_locator).click()
        self.wait_for_ajax()

    @property
    def test_cases(self):
        return [self.TestCaseItem(self.testsetup, web_element)
                for web_element in self.find_elements(*self._test_case_item_locator)]

    class TestCaseItem(PageRegion):

        _product_version_field_locator = (By.CSS_SELECTOR, '.product')
        _name_field_locator = (By.CSS_SELECTOR, '.title')
        _delete_button_locator = (By.CSS_SELECTOR, '.action-delete')

        @property
        def name(self):
            return self.find_element(*self._name_field_locator).text

        @property
        def product_version(self):
            return self.find_element(*self._product_version_field_locator).text

        def delete(self):
            self.find_element(*self._delete_button_locator).click()
