#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base_page import CaseConductorBasePage
from datetime import datetime


class CaseConductorCreateCasePage(CaseConductorBasePage):

    _page_title = 'Mozilla Case Conductor'

    _name_locator = 'id=id_name'
    _product_select_locator = 'id=id_product'
    _suite_select_locator = 'id=id_suite'
    _description_locator = 'id=id_description'
    _step1_instruction_locator = 'id=id_steps-0-instruction'
    _step1_result_locator = 'id=id_steps-0-expected_result'
    _submit_locator = 'css=#single-case-form .form-actions > button'
    _case_locator = u'css=#managecases .managelist article.item .title[title="%(case_name)s"]'

    def go_to_create_case_page(self):
        self.selenium.open('/manage/testcase/add/')
        self.is_the_current_page

    def create_case(self, name='Test Case', product='Test Product', suite=None, desc='This is a test case', step1_instruction='Test Case step 1 instruction', step1_result='Test Case step 1 expected result'):
        dt_string = datetime.utcnow().isoformat()
        case = {}
        case['name'] = u'%(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
        case['desc'] = u'%(desc)s created on %(dt_string)s' % {'desc': desc, 'dt_string': dt_string}
        case['locator'] = self._case_locator % {'case_name': case['name']}

        self.type(self._name_locator, case['name'])
        self.select(self._product_select_locator, product)
        if suite:
            self.select(self._suite_select_locator, suite)
        self.type(self._description_locator, case['desc'])
        self.type(self._step1_instruction_locator, step1_instruction)
        self.type(self._step1_result_locator, step1_result)
        self.click(self._submit_locator, wait_flag=True)

        return case
