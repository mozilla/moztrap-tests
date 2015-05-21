#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert

from pages.base_test import BaseTest
from pages.manage_versions_page import MozTrapManageVersionsPage


class TestManageVersionsPage(BaseTest):

    @pytest.mark.moztrap([3389, 3390])
    def test_that_user_can_create_and_delete_version(self, mozwebqa, login, product):
        manage_versions_pg = MozTrapManageVersionsPage(mozwebqa)

        version = self.create_version(mozwebqa, product)

        manage_versions_pg.filter_form.filter_by(lookup='version', value=version['name'])

        Assert.true(manage_versions_pg.is_element_present(*version['manage_locator']))

        manage_versions_pg.delete_version(name=version['name'], product_name=version['product']['name'])

        Assert.false(manage_versions_pg.is_element_present(*version['manage_locator']))

    @pytest.mark.moztrap(3391)
    def test_that_user_can_filter_version_by_name(self, mozwebqa, login, product):
        manage_versions_pg = MozTrapManageVersionsPage(mozwebqa)

        version = self.create_version(mozwebqa, product)

        filter_item = manage_versions_pg.filter_form.filter_by(lookup='version', value='Another Version')

        Assert.false(manage_versions_pg.is_element_present(*version['manage_locator']))

        filter_item.remove_filter()
        manage_versions_pg.filter_form.filter_by(lookup='version', value=version['name'])

        Assert.true(manage_versions_pg.is_element_present(*version['manage_locator']))

    @pytest.mark.moztrap(3392)
    def test_that_user_can_clone_version(self, mozwebqa, login, product):
        manage_versions_pg = MozTrapManageVersionsPage(mozwebqa)

        version = self.create_version(mozwebqa, product)

        manage_versions_pg.filter_form.filter_by(lookup='version', value=version['name'])

        cloned_version = manage_versions_pg.clone_version(name=version['name'], product_name=version['product']['name'])

        Assert.true(manage_versions_pg.is_element_present(*cloned_version['manage_locator']))

        manage_versions_pg.delete_version(name=cloned_version['name'], product_name=cloned_version['product_name'])

        Assert.false(manage_versions_pg.is_element_present(*cloned_version['manage_locator']))
