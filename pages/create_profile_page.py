#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from datetime import datetime

from base_page import MozTrapBasePage


class MozTrapCreateProfilePage(MozTrapBasePage):

    _page_title = 'MozTrap'

    _profile_name_locator = (By.ID, 'id_name')
    _select_category_locator = (By.CSS_SELECTOR, '#profile-add-form .itemlist .bulkselectitem[data-title="%(category_name)s"] .bulk-value')
    _delete_category_locator = (By.CSS_SELECTOR, '#profile-add-form .itemlist .bulkselectitem .action-delete[title="delete %(category_name)s"]')
    _add_category_locator = (By.CSS_SELECTOR, '#profile-add-form .itemlist .add-item .itemhead')
    _add_category_input_locator = (By.ID, 'new-category-name')
    _add_element_input_locator = (By.CSS_SELECTOR, '#profile-add-form .itemlist .bulkselectitem[data-title="%(category_name)s"] .listitem .add-element input[name="new-element-name"]')
    _new_element_locator = (By.CSS_SELECTOR, '#profile-add-form .itemlist .bulkselectitem[data-title="%(category_name)s"] .listitem .itembody .element[data-title="%(element_name)s"]')
    _submit_locator = (By.CSS_SELECTOR, '#profile-add-form .form-actions > button')
    _profile_locator = (By.CSS_SELECTOR, '#manageprofiles .listitem .title[title="%(profile_name)s"]')

    def go_to_create_profile_page(self):
        self.selenium.get(self.base_url + '/manage/profile/add/')
        self.is_the_current_page

    def create_profile(self, name='Test Profile', category_name='Test Category', element_name='Test Element'):
        dt_string = datetime.utcnow().isoformat()
        profile = {}
        profile['name'] = u'%(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
        profile['category'] = u'%(category_name)s %(dt_string)s' % {'category_name': category_name, 'dt_string': dt_string}
        profile['element'] = u'%(element_name)s %(dt_string)s' % {'element_name': element_name, 'dt_string': dt_string}
        profile['locator'] = (self._profile_locator[0], self._profile_locator[1] % {'profile_name': profile['name']})
        _select_category_locator = (self._select_category_locator[0], self._select_category_locator[1] % {'category_name': profile['category']})
        _add_element_input_locator = (self._add_element_input_locator[0], self._add_element_input_locator[1] % {'category_name': profile['category']})
        _new_element_locator = (self._new_element_locator[0], self._new_element_locator[1] % {'category_name': profile['category'], 'element_name': profile['element']})

        profile_name_field = self.selenium.find_element(*self._profile_name_locator)
        profile_name_field.send_keys(profile['name'])

        add_category = self.selenium.find_element(*self._add_category_locator)
        add_category.click()

        profile_category_field = self.selenium.find_element(*self._add_category_input_locator)
        profile_category_field.send_keys(profile['category'])
        profile_category_field.send_keys(Keys.RETURN)

        element_field = self.selenium.find_element(*_add_element_input_locator)
        element_field.send_keys(profile['element'])
        element_field.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.selenium.find_element(*_new_element_locator))
        self.selenium.find_element(*_select_category_locator).click()

        self.selenium.find_element(*self._submit_locator).click()

        return profile

    def delete_environment_category(self, category_name='Test Category'):
        _delete_category_locator = (self._delete_category_locator[0], self._delete_category_locator[1] % {'category_name': category_name})
        self.selenium.find_element(*_delete_category_locator).click()
