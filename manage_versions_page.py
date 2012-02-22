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

from base_page import CaseConductorBasePage


class CaseConductorManageVersionsPage(CaseConductorBasePage):

    _page_title = 'Mozilla Case Conductor'

    _version_manage_locator = u'css=#manageproductversions .listitem .title[title="%(product_name)s %(version_name)s"]'
    _version_homepage_locator = u'css=.runsdrill .runsfinder .productversions .colcontent .title[title="%(version_name)s"][data-product="%(product_name)s"])'
    _delete_version_locator = u'css=#manageproductversions .listitem .action-delete[title="delete %(product_name)s %(version_name)s"]'
    _clone_version_locator = u'css=#manageproductversions .listitem .action-clone[title="clone %(product_name)s %(version_name)s"]'
    _filter_input_locator = 'id=text-filter'
    _filter_suggestion_locator = u'css=#filter .textual .suggest .suggestion[data-type="version"][data-name="%(filter_name)s"]'
    _filter_locator = u'css=#filterform .filter-group input[data-name="version"][value="%(filter_name)s"]'

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
