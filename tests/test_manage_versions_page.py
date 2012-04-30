#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.manage_versions_page import MozTrapManageVersionsPage
from pages.base_test import BaseTest
from unittestzero import Assert


class TestManageVersionsPage(BaseTest):

    def test_that_user_can_create_and_delete_version(self, mozwebqa_logged_in):
        manage_versions_pg = MozTrapManageVersionsPage(mozwebqa_logged_in)

        version = self.create_version(mozwebqa_logged_in)

        manage_versions_pg.filter_versions_by_name(name=version['name'])

        Assert.true(manage_versions_pg.is_element_present(version['manage_locator']))

        manage_versions_pg.delete_version(name=version['name'], product_name=version['product']['name'])

        Assert.false(manage_versions_pg.is_element_present(version['manage_locator']))

        self.delete_product(mozwebqa_logged_in, version['product'])

    def test_that_user_can_filter_version_by_name(self, mozwebqa_logged_in):
        manage_versions_pg = MozTrapManageVersionsPage(mozwebqa_logged_in)

        version = self.create_version(mozwebqa_logged_in)

        manage_versions_pg.filter_versions_by_name(name='Another Version')

        Assert.false(manage_versions_pg.is_element_present(version['manage_locator']))

        manage_versions_pg.remove_name_filter(name='Another Version')
        manage_versions_pg.filter_versions_by_name(name=version['name'])

        Assert.true(manage_versions_pg.is_element_present(version['manage_locator']))

        self.delete_version(mozwebqa_logged_in, version, delete_product=True)

    def test_that_user_can_clone_version(self, mozwebqa_logged_in):
        manage_versions_pg = MozTrapManageVersionsPage(mozwebqa_logged_in)

        version = self.create_version(mozwebqa_logged_in)

        manage_versions_pg.filter_versions_by_name(name=version['name'])

        cloned_version = manage_versions_pg.clone_version(name=version['name'], product_name=version['product']['name'])

        Assert.true(manage_versions_pg.is_element_present(cloned_version['manage_locator']))

        manage_versions_pg.delete_version(name=cloned_version['name'], product_name=cloned_version['product_name'])

        Assert.false(manage_versions_pg.is_element_present(cloned_version['manage_locator']))

        self.delete_version(mozwebqa_logged_in, version, delete_product=True)
