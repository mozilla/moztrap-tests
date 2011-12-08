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
#                 Jonny Gerig Meyer <jonny@oddbird.net>
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

from home_page import CaseConductorHomePage
from base_test import BaseTest
from unittestzero import Assert


class TestHomepage(BaseTest):

    def test_that_user_can_login_and_logout(self, mozwebqa):
        home_pg = CaseConductorHomePage(mozwebqa)

        user = home_pg.testsetup.credentials["default"]
        home_pg.go_to_homepage_page(True, user)

        # TODO: uncomment when the id's are added
        #Assert.false(home_pg.is_user_logged_in)

        Assert.true(home_pg.is_user_logged_in)
        welcome_text = u"Welcome %s [Sign Out]" % user["name"]
        Assert.equal(home_pg.users_name_text, welcome_text)

        login_page = home_pg.logout()

        #Assert.false(home_pg.is_user_logged_in)
        Assert.true(login_page.is_register_visible)
        Assert.true(login_page.is_signin_visible)
