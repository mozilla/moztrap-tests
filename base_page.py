#!/usr/bin/env python
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from page import Page


class CaseConductorBasePage(Page):

    _user_name_locator = 'css=#accountnav .account-welcome .fn'
    _logout_locator = 'css=#accountnav .account-links .signout'

    @property
    def is_user_logged_in(self):
        return self.is_element_visible(self._user_name_locator)

    @property
    def users_name_text(self):
        return self.get_text(self._user_name_locator)

    def logout(self):
        self.click(self._logout_locator, True)
        from login_page import CaseConductorLoginPage
        return CaseConductorLoginPage(self.testsetup)
