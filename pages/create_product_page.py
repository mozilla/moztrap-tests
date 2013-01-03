#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import MozTrapBasePage


class MozTrapCreateProductPage(MozTrapBasePage):

    _page_title = 'Create Product'

    _name_locator = (By.ID, 'id_name')
    _version_locator = (By.ID, 'id_version')
    _profile_locator = (By.ID, 'id_profile')
    _description_locator = (By.ID, 'id_description')
    _submit_locator = (By.CSS_SELECTOR, '#product-add-form .form-actions > button')
    _product_locator = (By.CSS_SELECTOR, '#manageproducts .listitem .title[title="%(product_name)s"]')
    _version_manage_locator = (By.CSS_SELECTOR, '#manageproductversions .listitem .title[title="%(product_name)s %(version_name)s"]')
    _version_homepage_locator = (By.CSS_SELECTOR, '.runsdrill .runsfinder .productversions .colcontent .title[title="%(version_name)s"][data-product="%(product_name)s"]')

    def go_to_create_product_page(self):
        self.get_relative_path('/manage/product/add/')
        self.is_the_current_page

    def create_product(self, name='Test Product', version='Test Version', desc='This is a test product', profile=None):
        dt_string = datetime.utcnow().isoformat()
        product = {}
        product['name'] = u'%(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
        product['desc'] = u'%(desc)s created on %(dt_string)s' % {'desc': desc, 'dt_string': dt_string}
        product['locator'] = (self._product_locator[0], self._product_locator[1] % {'product_name': product['name']})
        product['version'] = {}
        product['version']['name'] = u'%(version)s %(dt_string)s' % {'version': version, 'dt_string': dt_string}
        product['version']['manage_locator'] = (self._version_manage_locator[0], self._version_manage_locator[1] % {'product_name': product['name'], 'version_name': product['version']['name']})
        product['version']['homepage_locator'] = (self._version_homepage_locator[0], self._version_homepage_locator[1] % {'product_name': product['name'], 'version_name': product['version']['name']})

        self.selenium.find_element(*self._name_locator).send_keys(product['name'])
        self.selenium.find_element(*self._version_locator).send_keys(product['version']['name'])
        self.selenium.find_element(*self._description_locator).send_keys(product['desc'])
        if profile:
            profile_select = Select(self.selenium.find_element(*self._profile_locator))
            profile_select.select_by_visible_text(profile)
        self.selenium.find_element(*self._submit_locator).click()

        return product
