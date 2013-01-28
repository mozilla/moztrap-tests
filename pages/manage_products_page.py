#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base_page import MozTrapBasePage
from pages.regions.filter import Filter


class MozTrapManageProductsPage(MozTrapBasePage):

    _page_title = 'Manage-Products'

    _delete_product_locator = (By.CSS_SELECTOR, '#manageproducts .listitem .controls .action-delete[title="delete %(product_name)s"]')

    @property
    def filter_form(self):
        return Filter(self.testsetup)

    def go_to_manage_products_page(self):
        self.get_relative_path('/manage/products/')
        self.is_the_current_page

    def delete_product(self, name='Test Product'):
        _delete_locator = (self._delete_product_locator[0], self._delete_product_locator[1] % {'product_name': name})

        self.selenium.find_element(*_delete_locator).click()
        self.wait_for_ajax()
