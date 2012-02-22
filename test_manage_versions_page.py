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

from manage_versions_page import CaseConductorManageVersionsPage
from base_test import BaseTest
from unittestzero import Assert


class TestManageVersionsPage(BaseTest):

    def test_that_user_can_create_and_delete_version(self, mozwebqa_logged_in):
        manage_versions_pg = CaseConductorManageVersionsPage(mozwebqa_logged_in)

        version = self.create_version(mozwebqa_logged_in)

        manage_versions_pg.filter_versions_by_name(name=version['name'])

        Assert.true(manage_versions_pg.is_element_present(version['manage_locator']))

        manage_versions_pg.delete_version(name=version['name'], product_name=version['product']['name'])

        Assert.false(manage_versions_pg.is_element_present(version['manage_locator']))

        self.delete_product(mozwebqa_logged_in, version['product'])

    def test_that_user_can_filter_version_by_name(self, mozwebqa_logged_in):
        manage_versions_pg = CaseConductorManageVersionsPage(mozwebqa_logged_in)

        version = self.create_version(mozwebqa_logged_in)

        manage_versions_pg.filter_versions_by_name(name='Another Version')

        Assert.false(manage_versions_pg.is_element_present(version['manage_locator']))

        manage_versions_pg.remove_name_filter(name='Another Version')
        manage_versions_pg.filter_versions_by_name(name=version['name'])

        Assert.true(manage_versions_pg.is_element_present(version['manage_locator']))

        self.delete_version(mozwebqa_logged_in, version, delete_product=True)

    def test_that_user_can_clone_version(self, mozwebqa_logged_in):
        manage_versions_pg = CaseConductorManageVersionsPage(mozwebqa_logged_in)

        version = self.create_version(mozwebqa_logged_in)

        manage_versions_pg.filter_versions_by_name(name=version['name'])

        cloned_version = manage_versions_pg.clone_version(name=version['name'], product_name=version['product']['name'])

        Assert.true(manage_versions_pg.is_element_present(cloned_version['manage_locator']))

        manage_versions_pg.delete_version(name=cloned_version['name'], product_name=cloned_version['product_name'])

        Assert.false(manage_versions_pg.is_element_present(cloned_version['manage_locator']))

        self.delete_version(mozwebqa_logged_in, version, delete_product=True)
