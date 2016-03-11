# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.base_test import BaseTest
from pages.manage_profiles_page import MozTrapManageProfilesPage


class TestManageProfilesPage(BaseTest):

    @pytest.mark.moztrap([154, 155])
    def test_that_user_can_create_and_delete_profile(self, base_url, selenium, login):
        from pages.create_profile_page import MozTrapCreateProfilePage
        manage_profiles_pg = MozTrapManageProfilesPage(base_url, selenium)
        create_profile_pg = MozTrapCreateProfilePage(base_url, selenium)

        profile = self.create_profile(base_url, selenium)

        manage_profiles_pg.filter_form.filter_by(lookup='name', value=profile['name'])

        assert manage_profiles_pg.is_element_present(*profile['locator'])

        manage_profiles_pg.delete_profile(name=profile['name'])

        assert not manage_profiles_pg.is_element_present(*profile['locator'])

        create_profile_pg.go_to_create_profile_page()
        create_profile_pg.delete_environment_category(category_name=profile['category'])
