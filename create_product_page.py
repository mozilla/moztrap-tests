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
# Contributor(s): Jonny Gerig Meyer <jonny@oddbird.net>
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
from datetime import datetime


class CaseConductorCreateProductPage(CaseConductorBasePage):

    _page_title = "Mozilla Case Conductor"

    _name_locator = "id=id_name"
    _profile_locator = "id=id_profile"
    _description_locator = "id=id_description"
    _submit_locator = "css=div.form-actions>button"

    def go_to_create_product_page(self, login=False, user="default"):
        self.selenium.open('/manage/product/add/')

        if login:
            from login_page import CaseConductorLoginPage
            login_pg = CaseConductorLoginPage(self.testsetup)
            login_pg.login(user)

        self.is_the_current_page

    def create_product(self, name="Test Product", desc="This is a test product", profile="Browser Testing Environments"):
        dt_string = datetime.utcnow().isoformat()
        product_name = name + " " + dt_string
        product_desc = desc + " created on " + dt_string

        self.type(self._name_locator, product_name)
        self.type(self._description_locator, product_desc)
        self.select(self._profile_locator, profile)
        self.click(self._submit_locator, wait_flag=True)

        return product_name

