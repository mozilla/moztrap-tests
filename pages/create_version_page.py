#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import MozTrapBasePage


class MozTrapCreateVersionPage(MozTrapBasePage):

    _page_title = 'Create Version'

    _version_name_locator = (By.ID, 'id_version')
    _product_select_locator = (By.ID, 'id_product')
    _submit_locator = (By.CSS_SELECTOR, '#productversion-add-form .form-actions > button')
    _version_manage_locator = (By.CSS_SELECTOR, '#manageproductversions .listitem .title[title="%(product_name)s %(version_name)s"]')
    _version_homepage_locator = (By.CSS_SELECTOR, '.runsdrill .runsfinder .productversions .colcontent .title[title="%(version_name)s"][data-product="%(product_name)s"])')

    def go_to_create_version_page(self):
        self.selenium.get(self.base_url + '/manage/productversion/add/')
        self.is_the_current_page

    def create_version(self, name='Test Version', product_name='Test Product'):
        dt_string = datetime.utcnow().isoformat()
        version = {}
        version['name'] = u'%(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
        version['manage_locator'] = (self._version_manage_locator[0], self._version_manage_locator[1] % {'product_name': product_name, 'version_name': version['name']})
        version['homepage_locator'] = (self._version_homepage_locator[0], self._version_homepage_locator[1] % {'product_name': product_name, 'version_name': version['name']})

        self.selenium.find_element(*self._version_name_locator).send_keys(version['name'])

        product_select = Select(self.selenium.find_element(*self._product_select_locator))
        product_select.select_by_visible_text(product_name)

        self.selenium.find_element(*self._submit_locator).click()

        return version

    @property
    def product_name_value(self):
        product_select = Select(self.find_element(*self._product_select_locator))
        return product_select.first_selected_option.text
