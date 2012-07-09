#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from pages.base_page import MozTrapBasePage


class MozTrapHomePage(MozTrapBasePage):

    _page_title = 'MozTrap'

    _select_locator = (By.CSS_SELECTOR, '.runsdrill .runsfinder .carousel .colcontent .title[title="%(item_name)s"]')
    _env_select_locator = (By.CSS_SELECTOR, '#runtests-environment-form .formfield[data-title="%(env_category)s"] select')
    _language_locator = (By.CSS_SELECTOR, '#runtests-environment-form .language-field select')
    _os_locator = (By.CSS_SELECTOR, '#runtests-environment-form .operating-system-field select')
    _submit_locator = (By.CSS_SELECTOR, '#runtests-environment-form .form-actions button[type="submit"]')

    def go_to_homepage_page(self):
        self.selenium.open('/')
        self.is_the_current_page

    def select_item(self, name):
        _select_locator = (self._select_locator[0], self._select_locator[1] % {'item_name': name})

        self.click(_select_locator)
        self.wait_for_ajax()

    def go_to_run_test(self, product_name, version_name, run_name, env_category, env_element):
        _env_select_locator = (self._env_select_locator[0], self._env_select_locator[1] % {'env_category': env_category})

        self.select_item(product_name)
        self.select_item(version_name)
        self.select_item(run_name)
        self.select(_env_select_locator, env_element)
        self.click(self._submit_locator, wait_flag=True)
