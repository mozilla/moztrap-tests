#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.base_page import MozTrapBasePage
from datetime import datetime


class MozTrapCreateVersionPage(MozTrapBasePage):

    _page_title = 'MozTrap'

    _version_name_locator = 'id=id_version'
    _product_select_locator = 'id=id_product'
    _submit_locator = 'css=#productversion-add-form .form-actions > button'
    _version_manage_locator = u'css=#manageproductversions .listitem .title[title="%(product_name)s %(version_name)s"]'
    _version_homepage_locator = u'css=.runsdrill .runsfinder .productversions .colcontent .title[title="%(version_name)s"][data-product="%(product_name)s"])'

    def go_to_create_version_page(self):
        self.selenium.open('/manage/productversion/add/')
        self.is_the_current_page

    def create_version(self, name='Test Version', product_name='Test Product'):
        dt_string = datetime.utcnow().isoformat()
        version = {}
        version['name'] = u'%(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
        version['manage_locator'] = self._version_manage_locator % {'product_name': product_name, 'version_name': version['name']}
        version['homepage_locator'] = self._version_homepage_locator % {'product_name': product_name, 'version_name': version['name']}

        self.type(self._version_name_locator, version['name'])
        self.select(self._product_select_locator, product_name)
        self.click(self._submit_locator, wait_flag=True)

        return version
