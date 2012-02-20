#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base_page import CaseConductorBasePage


class CaseConductorManageCyclesPage(CaseConductorBasePage):

    _page_title = 'Mozilla Case Conductor'

    _input_locator = 'id=text-filter'
    _update_list_locator = 'css=#filter .visual .content .form-actions button'
    _cycle_manage_locator = u'css=#managecycles .managelist article.item .title[title="%(cycle_name)s"]'
    _cycle_homepage_locator = u"css=.selectruns .finder .carousel .cycles .colcontent .title:contains(%(cycle_name)s)"
    _cloned_cycle_locator = u'css=#managecycles .managelist article.item .title[title^="Cloned on"][title$="%(cycle_name)s"]'
    _delete_cycle_locator = u'css=#managecycles .managelist article.item .title[title="%(cycle_name)s"] ~ .controls button[title="delete"]'
    _clone_cycle_locator = u'css=#managecycles .managelist article.item .title[title="%(cycle_name)s"] ~ .controls button[title="clone"]'
    _cycle_status_locator = u'xpath=//section[@id="managecycles"]//article[contains(@class,"item")]//h3[@title="%(cycle_name)s"]/../p[@class="status"]/button'
    _filter_suggestion_locator = u'css=#filter .textual .suggest a:contains(%(filter_name)s)'
    _filter_locator = u'css=#filter .visual .filter-group.keyword input[value="%(filter_name)s"]'

    def go_to_manage_cycles_page(self):
        self.selenium.open('/manage/testcycles/')
        self.is_the_current_page

    def delete_cycle(self, name='Test Cycle'):
        _delete_locator = self._delete_cycle_locator % {'cycle_name': name}

        self.click(_delete_locator)
        self.wait_for_ajax()

    def filter_cycles_by_name(self, name):
        _filter_suggestion_locator = self._filter_suggestion_locator % {'filter_name': name}
        _name_without_last_character = name[:-1]
        _name_last_character = name[-1]

        self.type(self._input_locator, _name_without_last_character)
        self.key_pressed(self._input_locator, _name_last_character)
        self.wait_for_element_present(_filter_suggestion_locator)
        self.click(_filter_suggestion_locator)
        self.wait_for_element_visible(self._update_list_locator)
        self.click(self._update_list_locator, wait_flag=True)

    def remove_name_filter(self, name):
        _filter_locator = self._filter_locator % {'filter_name': name.lower()}

        self.click(_filter_locator)
        self.wait_for_element_visible(self._update_list_locator)
        self.click(self._update_list_locator, wait_flag=True)

    def clone_cycle(self, name='Test Cycle'):
        _clone_cycle_locator = self._clone_cycle_locator % {'cycle_name': name}
        _cloned_cycle_locator = self._cloned_cycle_locator % {'cycle_name': name}
        cloned_cycle = {}

        self.click(_clone_cycle_locator)
        self.wait_for_element_visible(_cloned_cycle_locator)

        cloned_cycle['name'] = self.get_text(_cloned_cycle_locator)
        cloned_cycle['manage_locator'] = self._cycle_manage_locator % {'cycle_name': cloned_cycle['name']}
        cloned_cycle['homepage_locator'] = self._cycle_homepage_locator % {'cycle_name': cloned_cycle['name']}

        return cloned_cycle

    def activate_cycle(self, name='Test Cycle'):
        _cycle_status_locator = self._cycle_status_locator % {'cycle_name': name}

        self.click(_cycle_status_locator)
        self.wait_for_ajax()
