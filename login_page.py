#!/usr/bin/env python
#
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Case Conductor
#
# The Initial Developer of the Original Code is
# Mozilla Corp.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Bebe
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

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
