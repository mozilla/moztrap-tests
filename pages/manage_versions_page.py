#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base_page import MozTrapBasePage
from pages.regions.filter import Filter


class MozTrapManageVersionsPage(MozTrapBasePage):

    _page_title = 'Manage-Versions'

    _version_manage_locator = (By.CSS_SELECTOR, '#manageproductversions .listitem .title[title="%(product_name)s %(version_name)s"]')
    _version_homepage_locator = (By.CSS_SELECTOR, '.runsdrill .runsfinder .productversions .colcontent .title[title="%(version_name)s"][data-product="%(product_name)s"])')
    _create_version_button_locator = (By.CSS_SELECTOR, '#manageproductversions .create.single')
    _delete_version_locator = (By.CSS_SELECTOR, '#manageproductversions .listitem .action-delete[title="delete %(product_name)s %(version_name)s"]')
    _clone_version_locator = (By.CSS_SELECTOR, '#manageproductversions .listitem .action-clone[title="clone %(product_name)s %(version_name)s"]')

    @property
    def filter_form(self):
        return Filter(self.testsetup)

    def go_to_manage_versions_page(self):
        self.get_relative_path('/manage/productversions/')
        self.is_the_current_page

    def click_create_version_button(self):
        self.find_element(*self._create_version_button_locator).click()
        from pages.create_version_page import MozTrapCreateVersionPage
        return MozTrapCreateVersionPage(self.testsetup)

    def delete_version(self, name='Test Version', product_name='Test Product'):
        _delete_locator = (self._delete_version_locator[0], self._delete_version_locator[1] % {'product_name': product_name, 'version_name': name})

        self.selenium.find_element(*_delete_locator).click()
        self.wait_for_ajax()

    def clone_version(self, name='Test Version', product_name='Test Product'):
        _clone_version_locator = (self._clone_version_locator[0], self._clone_version_locator[1] % {'product_name': product_name, 'version_name': name})
        cloned_version = {}

        self.selenium.find_element(*_clone_version_locator).click()
        self.wait_for_ajax()

        cloned_version['product_name'] = product_name
        cloned_version['name'] = name + '.next'
        cloned_version['manage_locator'] = (self._version_manage_locator[0], self._version_manage_locator[1] % {'product_name': cloned_version['product_name'], 'version_name': cloned_version['name']})
        cloned_version['homepage_locator'] = (self._version_homepage_locator[0], self._version_homepage_locator[1] % {'product_name': cloned_version['product_name'], 'version_name': cloned_version['name']})

        return cloned_version
