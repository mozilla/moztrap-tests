#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.base_page import MozTrapBasePage
from datetime import datetime


class MozTrapCreateProfilePage(MozTrapBasePage):

    _page_title = 'MozTrap'

    _profile_name_locator = 'id=id_name'
    _select_category_locator = u'css=#profile-add-form .itemlist .bulkselectitem[data-title="%(category_name)s"] .bulk-value'
    _delete_category_locator = u'css=#profile-add-form .itemlist .bulkselectitem .action-delete[title="delete %(category_name)s"]'
    _add_category_locator = 'css=#profile-add-form .itemlist .add-item .itemhead'
    _add_category_input_locator = 'id=new-category-name'
    _add_element_input_locator = u'css=#profile-add-form .itemlist .bulkselectitem[data-title="%(category_name)s"] .listitem .add-element input[name="new-element-name"]'
    _new_element_locator = u'css=#profile-add-form .itemlist .bulkselectitem[data-title="%(category_name)s"] .listitem .itembody .element[data-title="%(element_name)s"]'
    _submit_locator = 'css=#profile-add-form .form-actions > button'
    _profile_locator = u'css=#manageprofiles .listitem .title[title="%(profile_name)s"]'

    def go_to_create_profile_page(self):
        self.open('/manage/profile/add/')
        self.is_the_current_page

    def create_profile(self, name='Test Profile', category_name='Test Category', element_name='Test Element'):
        dt_string = datetime.utcnow().isoformat()
        profile = {}
        profile['name'] = u'%(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
        profile['category'] = u'%(category_name)s %(dt_string)s' % {'category_name': category_name, 'dt_string': dt_string}
        profile['element'] = u'%(element_name)s %(dt_string)s' % {'element_name': element_name, 'dt_string': dt_string}
        profile['locator'] = self._profile_locator % {'profile_name': profile['name']}
        _select_category_locator = self._select_category_locator % {'category_name': profile['category']}
        _add_element_input_locator = self._add_element_input_locator % {'category_name': profile['category']}
        _new_element_locator = self._new_element_locator % {'category_name': profile['category'], 'element_name': profile['element']}

        self.type(self._profile_name_locator, profile['name'])
        self.click(self._add_category_locator)
        self.type(self._add_category_input_locator, profile['category'])
        self.selenium.key_down(self._add_category_input_locator, '13')
        self.wait_for_element_visible(_add_element_input_locator)
        self.type(_add_element_input_locator, profile['element'])
        self.selenium.key_down(_add_element_input_locator, '13')
        self.wait_for_element_visible(_new_element_locator)
        self.click(_select_category_locator)
        self.click(self._submit_locator, wait_flag=True)

        return profile

    def delete_environment_category(self, category_name='Test Category'):
        _delete_category_locator = self._delete_category_locator % {'category_name': category_name}

        self.click(_delete_category_locator)
        self.wait_for_ajax()
