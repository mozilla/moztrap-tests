#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base_page import MozTrapBasePage


class MozTrapLoginPage(MozTrapBasePage):

    _page_title = 'Login | MozTrap'

    _username_locator = 'id=id_username'
    _password_locator = 'id=id_password'
    _browserid_locator = 'id=browserid'
    _submit_locator = 'css=#loginform .form-actions > button'
    _register_locator = 'css=#loginform .form-actions > a'

    def login(self, user='default'):
        if type(user) is str:
            user = self.testsetup.credentials[user]

        self.type(self._username_locator, user['username'])
        self.type(self._password_locator, user['password'])
        self.click(self._submit_locator, True)
        from home_page import MozTrapHomePage
        return MozTrapHomePage(self.testsetup)

    def login_using_browserid(self, user='default'):
        from browserid import BrowserID
        from home_page import MozTrapHomePage

        if type(user) is str:
            user = self.testsetup.credentials[user]

        self.click(self._browserid_locator)

        browser_id = BrowserID(self.selenium, timeout=self.timeout)

        browser_id.sign_in(user['email'], user['password'])
        self.selenium.wait_for_page_to_load(timeout=self.timeout)

        return MozTrapHomePage(self.testsetup)

    @property
    def is_register_visible(self):
        return self.is_element_visible(self._register_locator)

    @property
    def is_signin_visible(self):
        return self.is_element_visible(self._submit_locator)
