#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import MozTrapBasePage
from pages.regions.multiselect_widget import MultiselectWidget


class MozTrapCreateSuitePage(MozTrapBasePage):

    _page_title = 'Create Suite'

    _name_locator = (By.ID, 'id_name')
    _product_select_locator = (By.ID, 'id_product')
    _description_locator = (By.ID, 'id_description')
    _status_select_locator = (By.ID, 'id_status')
    _submit_locator = (By.CSS_SELECTOR, '#suite-add-form .form-actions button[type="submit"]')
    _suite_locator = (By.CSS_SELECTOR, '#managesuites .itemlist .listitem .title[title="%(suite_name)s"]')

    def go_to_create_suite_page(self):
        self.get_relative_path('/manage/suite/add/')
        self.is_the_current_page

    def create_suite(self, name='Test Suite', product='Test Product', desc='This is a test suite', status='active', case_list=None):
        dt_string = datetime.utcnow().isoformat()
        suite = {}
        suite['name'] = u'%(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
        suite['desc'] = u'%(desc)s created on %(dt_string)s' % {'desc': desc, 'dt_string': dt_string}
        suite['locator'] = (self._suite_locator[0], self._suite_locator[1] % {'suite_name': suite['name']})

        self.selenium.find_element(*self._name_locator).send_keys(suite['name'])
        product_select = Select(self.selenium.find_element(*self._product_select_locator))
        product_select.select_by_visible_text(product)

        self.selenium.find_element(*self._description_locator).send_keys(suite['desc'])

        status_select = Select(self.selenium.find_element(*self._status_select_locator))
        status_select.select_by_visible_text(status)

        if case_list:
            self.multiselect_widget.include_items(case_list)
        self.selenium.find_element(*self._submit_locator).click()

        return suite

    @property
    def product_name_value(self):
        product_select = self.find_element(*self._product_select_locator)
        return product_select.find_element(By.CSS_SELECTOR, 'option:checked').text

    @property
    def multiselect_widget(self):
        return MultiselectWidget(self.testsetup)
