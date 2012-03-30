#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base_page import MozTrapBasePage


class MozTrapManageVersionsPage(MozTrapBasePage):

    _page_title = 'MozTrap'

    _version_manage_locator = u'css=#manageproductversions .listitem .title[title="%(product_name)s %(version_name)s"]'
    _version_homepage_locator = u'css=.runsdrill .runsfinder .productversions .colcontent .title[title="%(version_name)s"][data-product="%(product_name)s"])'
    _delete_version_locator = u'css=#manageproductversions .listitem .action-delete[title="delete %(product_name)s %(version_name)s"]'
    _clone_version_locator = u'css=#manageproductversions .listitem .action-clone[title="clone %(product_name)s %(version_name)s"]'
    _filter_input_locator = 'id=text-filter'
    _filter_suggestion_locator = u'css=#filter .textual .suggest .suggestion[data-type="version"][data-name="%(filter_name)s"]'
    _filter_locator = u'css=#filterform .filter-group input[data-name="version"][value="%(filter_name)s"]:checked'

    def go_to_manage_versions_page(self):
        self.selenium.open('/manage/productversions/')
        self.is_the_current_page

    def delete_version(self, name='Test Version', product_name='Test Product'):
        _delete_locator = self._delete_version_locator % {'product_name': product_name, 'version_name': name}

        self.click(_delete_locator)
        self.wait_for_ajax()

    def filter_versions_by_name(self, name):
        _filter_locator = self._filter_locator % {'filter_name': name.lower()}
        _filter_suggestion_locator = self._filter_suggestion_locator % {'filter_name': name}
        _name_without_last_character = name[:-1]
        _name_last_character = name[-1]

        self.type(self._filter_input_locator, _name_without_last_character)
        self.key_pressed(self._filter_input_locator, _name_last_character)
        self.wait_for_element_present(_filter_suggestion_locator)
        self.click(_filter_suggestion_locator)
        self.wait_for_element_present(_filter_locator)
        self.wait_for_ajax()

    def remove_name_filter(self, name):
        _filter_locator = self._filter_locator % {'filter_name': name.lower()}

        self.click(_filter_locator)
        self.wait_for_ajax()

    def clone_version(self, name='Test Version', product_name='Test Product'):
        _clone_version_locator = self._clone_version_locator % {'product_name': product_name, 'version_name': name}
        cloned_version = {}

        self.click(_clone_version_locator)
        self.wait_for_ajax()

        cloned_version['product_name'] = product_name
        cloned_version['name'] = name + '.next'
        cloned_version['manage_locator'] = self._version_manage_locator % {'product_name': cloned_version['product_name'], 'version_name': cloned_version['name']}
        cloned_version['homepage_locator'] = self._version_homepage_locator % {'product_name': cloned_version['product_name'], 'version_name': cloned_version['name']}

        return cloned_version
