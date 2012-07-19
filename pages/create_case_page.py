#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import MozTrapBasePage


class MozTrapCreateCasePage(MozTrapBasePage):

    _page_title = 'MozTrap'

    _name_locator = (By.ID, 'id_name')
    _product_select_locator = (By.ID, 'id_product')
    _version_select_locator = (By.ID, 'id_productversion')
    _suite_select_locator = (By.ID, 'id_initial_suite')
    _description_locator = (By.ID, 'id_description')
    _step1_instruction_locator = (By.ID, 'id_steps-0-instruction')
    _step1_result_locator = (By.ID, 'id_steps-0-expected')
    _status_select_locator = (By.ID, 'id_status')
    _submit_locator = (By.CSS_SELECTOR, '#single-case-add .form-actions button[type="submit"]')
    _case_locator = (By.CSS_SELECTOR, '#managecases .itemlist .listitem .title[title="%(case_name)s"]')

    def go_to_create_case_page(self):
        self.selenium.get(self.base_url + '/manage/case/add/')
        self.is_the_current_page

    def create_case(self, name='Test Case', product='Test Product', version='Test Version', suite=None, desc='This is a test case', step1_instruction='Test Case step 1 instruction', step1_result='Test Case step 1 expected result', status='active'):
        dt_string = datetime.utcnow().isoformat()
        case = {}
        case['name'] = u'%(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
        case['desc'] = u'%(desc)s created on %(dt_string)s' % {'desc': desc, 'dt_string': dt_string}
        case['locator'] = (self._case_locator[0], self._case_locator[1] % {'case_name': case['name']})

        name_field = self.selenium.find_element(*self._name_locator)
        name_field.send_keys(case['name'])

        product_select = Select(self.selenium.find_element(*self._product_select_locator))
        product_select.select_by_visible_text(product)

        version_select = Select(self.selenium.find_element(*self._version_select_locator))
        version_select.select_by_visible_text(product)

        if suite:
            suite_select = Select(self.selenium.find_element(*self._suite_select_locator))
            suite_select.select_by_visible_text(suite)

        self.selenium.find_element(*self._description_locator).send_keys(case['desc'])
        self.selenium.find_element(*self._step1_instruction_locator).send_keys(step1_instruction)
        self.selenium.find_element(*self._step1_result_locator).send_keys(step1_result)

        status_select = Select(self.selenium.find_element(*self._status_select_locator))
        status_select.select_by_visible_text(status)

        self.selenium.find_element(*self._submit_locator).click()

        return case
