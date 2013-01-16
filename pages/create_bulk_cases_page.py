#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import MozTrapBasePage


class MozTrapCreateBulkCasesPage(MozTrapBasePage):

    _page_title = 'Create Bulk Case'

    _product_select_locator = (By.ID, 'id_product')
    _version_select_locator = (By.ID, 'id_productversion')
    _suite_select_locator = (By.ID, 'id_suite')
    _cases_description_locator = (By.ID, 'id_cases')
    _status_select_locator = (By.ID, 'id_status')
    _submit_locator = (By.CSS_SELECTOR, '#bulk-case-add button[name="save"]')
    _case_locator = (By.CSS_SELECTOR, '#managecases .itemlist .listitem .title[title="%(case_name)s"]')

    def go_to_create_bulk_cases_page(self):
        self.selenium.get(self.base_url + '/manage/case/add/bulk/')
        self.is_the_current_page

    def create_bulk_cases(
            self, name='Test Case', product='Test Product', version='Test Version',
            suite=None, desc='This is a test case', status='active',
            step1_instruction='Test Case step 1 instruction',
            step1_result='Test Case step 1 expected result', cases_amount=2):

        cases = []
        for case in xrange(cases_amount):
            dt_string = datetime.utcnow().isoformat()
            case = {}
            case['name'] = u'Test that %(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
            case['desc'] = u'%(desc)s created on %(dt_string)s' % {'desc': desc, 'dt_string': dt_string}
            case['locator'] = (self._case_locator[0], self._case_locator[1] % {'case_name': case['name']})
            cases.append(case)

        desc_str = []
        for case in cases:
            desc_str.append('%s \n %s \n When %s \n Then %s \n' % (case['name'], case['desc'], step1_instruction, step1_result))
        cases_desc = '\n'.join(desc_str)

        product_select = Select(self.selenium.find_element(*self._product_select_locator))
        product_select.select_by_visible_text(product)

        version_select = Select(self.selenium.find_element(*self._version_select_locator))
        version_select.select_by_visible_text(version)

        if suite:
            suite_select = Select(self.selenium.find_element(*self._suite_select_locator))
            suite_select.select_by_visible_text(suite)

        self.selenium.find_element(*self._cases_description_locator).send_keys(cases_desc)

        status_select = Select(self.selenium.find_element(*self._status_select_locator))
        status_select.select_by_visible_text(status)

        self.selenium.find_element(*self._submit_locator).click()

        return cases
