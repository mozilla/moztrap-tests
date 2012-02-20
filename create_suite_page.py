#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base_page import CaseConductorBasePage
from datetime import datetime


class CaseConductorCreateSuitePage(CaseConductorBasePage):

    _page_title = 'Mozilla Case Conductor'

    _name_locator = 'id=id_name'
    _product_select_locator = 'id=id_product'
    _description_locator = 'id=id_description'
    _submit_locator = 'css=#suite-form .form-actions > button'
    _suite_locator = u'css=#managesuites .managelist article.item .title[title="%(suite_name)s"]'

    def go_to_create_suite_page(self):
        self.selenium.open('/manage/testsuite/add/')
        self.is_the_current_page

    def create_suite(self, name='Test Suite', product='Test Product', desc='This is a test suite'):
        dt_string = datetime.utcnow().isoformat()
        suite = {}
        suite['name'] = u'%(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
        suite['desc'] = u'%(desc)s created on %(dt_string)s' % {'desc': desc, 'dt_string': dt_string}
        suite['locator'] = self._suite_locator % {'suite_name': suite['name']}

        self.type(self._name_locator, suite['name'])
        self.select(self._product_select_locator, product)
        self.type(self._description_locator, suite['desc'])
        self.click(self._submit_locator, wait_flag=True)

        return suite
