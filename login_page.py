#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base_page import CaseConductorBasePage


class CaseConductorLoginPage(CaseConductorBasePage):

    _page_title = "Mozilla Case Conductor"

    _signin_locator = "css=nav.meta>ul>li>a:nth(0)"
    _register_locator = "css=nav.meta>ul>li>a:nth(1)"
    _account_locator = "css=nav.meta>ul"

    _email_locator = "id=id_email"
    _password_locator = "id=id_password"
    _submit_locator = "css=div.form-actions>button"

    def login(self, user="default"):
        if type(user) is str:
            user = self.testsetup.credentials[user]

        self.type(self._email_locator, user['email'])
        self.type(self._password_locator, user['password'])
        self.click(self._submit_locator, True)
        from home_page import CaseConductorHomePage
        return CaseConductorHomePage(self.testsetup)

    @property
    def is_register_visible(self):
        return self.is_element_visible(self._register_locator)

    @property
    def is_signin_visible(self):
        return self.is_element_visible(self._signin_locator)

    @property
    def account_text(self):
        return self.get_text(self._account_locator)
