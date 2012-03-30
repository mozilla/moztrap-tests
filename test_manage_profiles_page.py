#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from manage_profiles_page import MozTrapManageProfilesPage
from base_test import BaseTest
from unittestzero import Assert


class TestManageProfilesPage(BaseTest):

    def test_that_user_can_create_and_delete_profile(self, mozwebqa_logged_in):
        from create_profile_page import MozTrapCreateProfilePage
        manage_profiles_pg = MozTrapManageProfilesPage(mozwebqa_logged_in)
        create_profile_pg = MozTrapCreateProfilePage(mozwebqa_logged_in)

        profile = self.create_profile(mozwebqa_logged_in)

        manage_profiles_pg.filter_profiles_by_name(name=profile['name'])

        Assert.true(manage_profiles_pg.is_element_present(profile['locator']))

        manage_profiles_pg.delete_profile(name=profile['name'])

        Assert.false(manage_profiles_pg.is_element_present(profile['locator']))

        create_profile_pg.go_to_create_profile_page()
        create_profile_pg.delete_environment_category(category_name=profile['category'])
