#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base_page import CaseConductorBasePage
from datetime import datetime


class CaseConductorCreateProductPage(CaseConductorBasePage):

    _page_title = 'Mozilla Case Conductor'

    _name_locator = 'id=id_name'
    _version_locator = 'id=id_version'
    _profile_locator = 'id=id_profile'
    _description_locator = 'id=id_description'
    _submit_locator = 'css=#product-add-form .form-actions > button'
    _product_locator = u'css=#manageproducts .listitem .title:contains(%(product_name)s)'
    _version_manage_locator = u'css=#manageproductversions .listitem .title[title="%(product_name)s %(version_name)s"]'
    _version_homepage_locator = u'css=.runsdrill .runsfinder .productversions .colcontent .title[title="%(version_name)s"][data-product="%(product_name)s"]'

    def go_to_create_product_page(self):
        self.selenium.open('/manage/product/add/')
        self.is_the_current_page

    def create_product(self, name='Test Product', version='Test Version', desc='This is a test product', profile=None):
        dt_string = datetime.utcnow().isoformat()
        product = {}
        product['name'] = u'%(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
        product['desc'] = u'%(desc)s created on %(dt_string)s' % {'desc': desc, 'dt_string': dt_string}
        product['locator'] = self._product_locator % {'product_name': product['name']}
        product['version'] = {}
        product['version']['name'] = u'%(version)s %(dt_string)s' % {'version': version, 'dt_string': dt_string}
        product['version']['manage_locator'] = self._version_manage_locator % {'product_name': product['name'], 'version_name': product['version']['name']}
        product['version']['homepage_locator'] = self._version_homepage_locator % {'product_name': product['name'], 'version_name': product['version']['name']}

        self.type(self._name_locator, product['name'])
        self.type(self._version_locator, product['version']['name'])
        self.type(self._description_locator, product['desc'])
        if profile:
            self.select(self._profile_locator, profile)
        self.click(self._submit_locator, wait_flag=True)

        return product
