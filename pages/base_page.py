#!/usr/bin/env python
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page


class MozTrapBasePage(Page):

    _user_name_locator = (By.CSS_SELECTOR, '#accountnav .account-welcome .fn')
    _logout_locator = (By.CSS_SELECTOR, '#accountnav .account-links .signout')

    @property
    def is_user_logged_in(self):
        return self.is_element_visible(*self._logout_locator)

    @property
    def users_name_text(self):
        return self.selenium.find_element(*self._user_name_locator).text

    def logout(self):
        self.selenium.find_element(*self._logout_locator).click()
        from login_page import MozTrapLoginPage
        return MozTrapLoginPage(self.testsetup)

    @property
    def header(self):
        return self.Header(testsetup)

    class Header(Page):
        
        pass