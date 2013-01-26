#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import MozTrapBasePage
from pages.page import Page


class MozTrapEditSuitePage(MozTrapBasePage):

    _page_title = 'Edit Suite'

    _product_field_locator = (By.CSS_SELECTOR, '.formfield.product-field .value')
    _available_case_item_locator = (By.CSS_SELECTOR, '.multiunselected .selectitem')
    _included_case_item_locator = (By.CSS_SELECTOR, '.multiselected .selectitem')
    _included_cases_box_locator = (By.CSS_SELECTOR, '.multiselected .select')
    _include_selected_cases_button_locator = (By.CSS_SELECTOR, '#suite-edit-form .action-include')
    _loading_available_cases_locator = (By.CSS_SELECTOR, '.multiunselected .select .overlay')
    _loading_included_cases_locator = (By.CSS_SELECTOR, '.multiselected .select .overlay')
    _save_suite_button_locator = (By.CSS_SELECTOR, '#suite-edit-form .form-actions > button')

    @property
    def is_product_field_readonly(self):
        product_field = self.selenium.find_element(*self._product_field_locator)
        if product_field.tag_name == u'select' and product_field.is_enabled():
            return False
        else:
            return True

    @property
    def available_cases(self):
        self.wait_for_element_not_present(*self._loading_available_cases_locator)
        return [self.TestCaseItem(self.testsetup, case_item)
                for case_item in self.selenium.find_elements(*self._available_case_item_locator)]

    @property
    def has_included_cases(self):
        self.wait_for_element_not_present(*self._loading_included_cases_locator)
        return self.is_element_present(*self._included_case_item_locator)

    @property
    def included_cases(self):
        self.wait_for_element_not_present(*self._loading_included_cases_locator)
        return [self.TestCaseItem(self.testsetup, case_item)
                for case_item in self.selenium.find_elements(*self._included_case_item_locator)]

    def include_cases_to_suite(self, case_name_list, save=True):
        #wait till available and included cases are not loaded
        self.wait_for_element_not_present(*self._loading_available_cases_locator)
        self.wait_for_element_not_present(*self._loading_included_cases_locator)
        include_button = self.selenium.find_element(*self._include_selected_cases_button_locator)

        available_items = self.available_cases
        items_to_add = [item for name in reversed(case_name_list) for item in available_items
                        if name == item.name]

        for item in items_to_add:
            item.select()
            include_button.click()

        if save:
            self.selenium.find_element(*self._save_suite_button_locator).click()


    class TestCaseItem(Page):

        _select_item_locator = (By.CSS_SELECTOR, '.bulk-type')
        _item_title_locator = (By.CSS_SELECTOR, '.title')

        def __init__(self, testsetup, web_element):
            Page.__init__(self, testsetup)
            self.selenium = web_element

        @property
        def name(self):
            return self.selenium.find_element(*self._item_title_locator).text

        def select(self):
            self.selenium.find_element(*self._select_item_locator).click()
