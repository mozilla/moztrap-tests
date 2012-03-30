#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base_page import MozTrapBasePage


class MozTrapManageCasesPage(MozTrapBasePage):

    _page_title = 'MozTrap'

    _delete_case_locator = u'css=#managecases .itemlist .listitem[data-title="%(case_name)s"] .action-delete'
    _case_status_locator = u'css=#managecases .itemlist .listitem[data-title="%(case_name)s"] .status-action'
    _filter_input_locator = 'id=text-filter'
    _filter_suggestion_locator = u'css=#filter .textual .suggest .suggestion[data-type="name"][data-name="%(filter_name)s"]'
    _filter_locator = u'css=#filterform .filter-group input[data-name="name"][value="%(filter_name)s"]:checked'

    def go_to_manage_cases_page(self):
        self.selenium.open('/manage/cases/')
        self.is_the_current_page

    def delete_case(self, name='Test Case'):
        _delete_locator = self._delete_case_locator % {'case_name': name}

        self.click(_delete_locator)
        self.wait_for_ajax()

    def filter_cases_by_name(self, name):
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

    def activate_case(self, name='Test Case'):
        _case_status_locator = self._case_status_locator % {'case_name': name}

        self.click(_case_status_locator)
        self.wait_for_ajax()
