#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base_page import CaseConductorBasePage
from datetime import datetime


class CaseConductorCreateProductPage(CaseConductorBasePage):

    _page_title = "Mozilla Case Conductor"

    _name_locator = "id=id_name"
    _profile_locator = "id=id_profile"
    _description_locator = "id=id_description"
    _submit_locator = "css=div.form-actions>button"
    _product_locator = u'css=#manageproducts article.item .title:contains(%(product_name)s)'

    def go_to_create_product_page(self):
        self.selenium.open('/manage/product/add/')
        self.is_the_current_page

    def create_product(self, name="Test Product", desc="This is a test product", profile="Browser Testing Environments"):
        dt_string = datetime.utcnow().isoformat()
        product = {}
        product['name'] = name + ' ' + dt_string
        product['desc'] = desc + ' created on ' + dt_string
        product['locator'] = self._product_locator % {'product_name': product['name']}

        self.type(self._name_locator, product['name'])
        self.type(self._description_locator, product['desc'])
        self.select(self._profile_locator, profile)
        self.click(self._submit_locator, wait_flag=True)

        return product
