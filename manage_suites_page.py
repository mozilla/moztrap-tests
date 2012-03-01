#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base_page import CaseConductorBasePage


class CaseConductorManageSuitesPage(CaseConductorBasePage):

    _page_title = 'Mozilla Case Conductor'

    _input_locator = 'id=text-filter'
    _update_list_locator = 'css=#filter .visual .content .form-actions button'
    _delete_suite_locator = u'css=#managesuites .managelist article.item .title[title="%(suite_name)s"] ~ .controls button[title="delete"]'
    _suite_status_locator = u'xpath=//section[@id="managesuites"]//article[contains(@class,"item")]//h3[@title="%(suite_name)s"]/../p[@class="status"]/button'
    _filter_suggestion_locator = u'css=#filter .textual .suggest a:contains(%(filter_name)s)'
    _filter_locator = u'css=#filter .visual .filter-group.keyword input[value="%(filter_name)s"]'

    def go_to_manage_suites_page(self):
        self.selenium.open('/manage/testsuites/')
        self.is_the_current_page

    def delete_suite(self, name='Test Suite'):
        _delete_locator = self._delete_suite_locator % {'suite_name': name}

        self.click(_delete_locator)
        self.wait_for_ajax()

    def filter_suites_by_name(self, name):
        _filter_suggestion_locator = self._filter_suggestion_locator % {'filter_name': name}
        _name_without_last_character = name[:-1]
        _name_last_character = name[-1]

        self.type(self._input_locator, _name_without_last_character)
        self.key_pressed(self._input_locator, _name_last_character)
        self.wait_for_element_present(_filter_suggestion_locator)
        self.click(_filter_suggestion_locator)
        self.wait_for_element_visible(self._update_list_locator)
        self.click(self._update_list_locator, wait_flag=True)

    def activate_suite(self, name='Test Suite'):
        _suite_status_locator = self._suite_status_locator % {'suite_name': name}

        self.click(_suite_status_locator)
        self.wait_for_ajax()
