#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base_page import MozTrapBasePage
from pages.regions.filter import Filter


class MozTrapManageProfilesPage(MozTrapBasePage):

    _page_title = 'Manage-Environments'

    _delete_profile_locator = (By.CSS_SELECTOR, '#manageprofiles .listitem .action-delete[title="delete %(profile_name)s"]')

    @property
    def filter_form(self):
        return Filter(self.testsetup)

    def go_to_manage_profiles_page(self):
        self.selenium.get(self.base_url + '/manage/profiles/')
        self.is_the_current_page

    def delete_profile(self, name='Test Profile'):
        _delete_locator = (self._delete_profile_locator[0], self._delete_profile_locator[1] % {'profile_name': name})

        self.selenium.find_element(*_delete_locator).click()
        self.wait_for_ajax()
