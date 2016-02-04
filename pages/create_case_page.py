# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from pages.base_page import MozTrapBasePage


class MozTrapCreateCasePage(MozTrapBasePage):

    _page_title = 'Create Case'

    _name_locator = (By.ID, 'id_name')
    _product_select_locator = (By.ID, 'id_product')
    _version_select_locator = (By.ID, 'id_productversion')
    _suite_select_locator = (By.ID, 'id_suite')
    _description_locator = (By.ID, 'id_description')
    _step1_instruction_locator = (By.ID, 'id_steps-0-instruction')
    _step1_result_locator = (By.ID, 'id_steps-0-expected')
    _status_select_locator = (By.ID, 'id_status')
    _tag_field_locator = (By.ID, 'id_add_tags')
    _tag_field_suggest_locator = (By.CSS_SELECTOR, '.suggest')
    _tag_item_locator = (By.CSS_SELECTOR, '.tag-item')
    _submit_locator = (By.CSS_SELECTOR, '#single-case-add .form-actions button[type="submit"]')
    _case_locator = (By.CSS_SELECTOR, '#managecases .itemlist .listitem .title[title="%(case_name)s"]')

    def go_to_create_case_page(self):
        self.selenium.get(self.base_url + '/manage/case/add/')
        self.is_the_current_page

    def create_case(self, test_case):
        test_case['locator'] = (self._case_locator[0],
                                self._case_locator[1] % {'case_name': test_case['name']})

        name_field = self.selenium.find_element(*self._name_locator)
        name_field.send_keys(test_case['name'])

        product_select = Select(self.selenium.find_element(*self._product_select_locator))
        product_select.select_by_visible_text(test_case['product']['name'])

        version_select = Select(self.selenium.find_element(*self._version_select_locator))
        version_select.select_by_visible_text(test_case['version']['name'])

        if test_case.get('suite'):
            suite_select = Select(self.selenium.find_element(*self._suite_select_locator))
            suite_select.select_by_visible_text(test_case['suite'])

        desc_field = self.selenium.find_element(*self._description_locator)
        desc_field.send_keys(test_case['description'])

        step_field = self.selenium.find_element(*self._step1_instruction_locator)
        step_field.send_keys(test_case['step1_instruction'])

        result_field = self.selenium.find_element(*self._step1_result_locator)
        result_field.send_keys(test_case['step1_result'])

        status_select = Select(self.selenium.find_element(*self._status_select_locator))
        status_select.select_by_visible_text(test_case['status'])

        if test_case.get('tag'):
            tag_field = self.selenium.find_element(*self._tag_field_locator)
            tag_field.send_keys(test_case['tag']['name'])

            # to add new tag we need to wait for suggest list to appear
            self.wait_for_element_to_be_visible(*self._tag_field_suggest_locator)
            tag_field.send_keys(Keys.RETURN)
            self.wait_till_tag_is_attached()

        self.selenium.find_element(*self._submit_locator).click()

        return test_case

    @property
    def product_value(self):
        product_select = self.find_element(*self._product_select_locator)
        return product_select.find_element(By.CSS_SELECTOR, 'option:checked').text

    @property
    def product_version_value(self):
        version_select = self.find_element(*self._version_select_locator)
        return version_select.find_element(By.CSS_SELECTOR, 'option:checked').text

    @property
    def suite_value(self):
        suite_select = self.find_element(*self._suite_select_locator)
        return suite_select.find_element(By.CSS_SELECTOR, 'option:checked').text

    def wait_till_tag_is_attached(self):
        self.wait_for_element_to_be_visible(*self._tag_item_locator)
