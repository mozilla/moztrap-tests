#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base_page import CaseConductorBasePage
from datetime import datetime


class CaseConductorCreateCyclePage(CaseConductorBasePage):

    _page_title = 'Mozilla Case Conductor'

    _name_locator = 'id=id_name'
    _product_select_locator = 'id=id_product'
    _description_locator = 'id=id_description'
    _start_date_locator = 'id=id_start_date'
    _end_date_locator = 'id=id_end_date'
    _submit_locator = 'css=#cycle-form .form-actions > button'
    _cycle_manage_locator = u'css=#managecycles .managelist article.item .title[title="%(cycle_name)s"]'
    _cycle_homepage_locator = u"css=.selectruns .finder .carousel .cycles .colcontent .title:contains(%(cycle_name)s)"

    def go_to_create_cycle_page(self):
        self.selenium.open('/manage/testcycle/add/')
        self.is_the_current_page

    def create_cycle(self, name='Test Cycle', product='Test Product', desc='This is a test cycle', start_date='2011-01-01', end_date='2012-12-31'):
        dt_string = datetime.utcnow().isoformat()
        cycle = {}
        cycle['name'] = u'%(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
        cycle['desc'] = u'%(desc)s created on %(dt_string)s' % {'desc': desc, 'dt_string': dt_string}
        cycle['manage_locator'] = self._cycle_manage_locator % {'cycle_name': cycle['name']}
        cycle['homepage_locator'] = self._cycle_homepage_locator % {'cycle_name': cycle['name']}

        self.type(self._name_locator, cycle['name'])
        self.select(self._product_select_locator, product)
        self.type(self._description_locator, cycle['desc'])
        self.type(self._start_date_locator, start_date)
        self.type(self._end_date_locator, end_date)
        self.click(self._submit_locator, wait_flag=True)

        return cycle
