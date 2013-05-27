#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import MozTrapBasePage


class MozTrapLoginPage(MozTrapBasePage):

    _page_title = 'Login'

    _username_locator = (By.ID, 'id_username')
    _password_locator = (By.ID, 'id_password')
    _browserid_locator = (By.ID, 'browserid')
    _submit_locator = (By.CSS_SELECTOR, '#loginform .form-actions > button')
    _register_locator = (By.CSS_SELECTOR, '#loginform .form-actions > a')

    def go_to_login_page(self):
        self.get_relative_path('/users/login/')
        self.is_the_current_page

    def login(self, user='default'):
        from home_page import MozTrapHomePage

        if type(user) is str:
            user = self.testsetup.credentials[user]

        from browserid import BrowserID
        self.selenium.find_element(*self._browserid_locator).click()
        browser_id = BrowserID(self.selenium, timeout=self.timeout)
        browser_id.sign_in(user['email'], user['password'])

        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.header.is_user_logged_in)

        return MozTrapHomePage(self.testsetup)

    @property
    def is_browserid_visible(self):
        return self.is_element_visible(*self._browserid_locator)

    @property
    def is_register_visible(self):
        return self.is_element_visible(*self._register_locator)

    @property
    def is_signin_visible(self):
        return self.is_element_visible(*self._submit_locator)
