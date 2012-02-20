#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base_page import CaseConductorBasePage
from datetime import datetime


class CaseConductorCreateRunPage(CaseConductorBasePage):

    _page_title = 'Mozilla Case Conductor'

    _name_locator = 'id=id_name'
    _cycle_select_locator = 'id=id_test_cycle'
    _description_locator = 'id=id_description'
    _start_date_locator = 'id=id_start_date'
    _end_date_locator = 'id=id_end_date'
    _suite_select_locator = 'id=id_suites'
    _submit_locator = 'css=#run-form .form-actions > button'
    _run_manage_locator = u'css=#manageruns .managelist article.item .title[title="%(run_name)s"]'
    _run_homepage_locator = u"css=.selectruns .finder .carousel .runs .colcontent .title:contains(%(run_name)s)"
    _run_tests_button_locator = u"css=.environment .form-actions button:contains(run tests in %(run_name)s!)"

    def go_to_create_run_page(self):
        self.selenium.open('/manage/testrun/add/')
        self.is_the_current_page

    def create_run(self, name='Test Run', cycle='Test Cycle', desc='This is a test run', start_date='2011-01-01', end_date='2012-12-31', suite=None):
        dt_string = datetime.utcnow().isoformat()
        run = {}
        run['name'] = u'%(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
        run['desc'] = u'%(desc)s created on %(dt_string)s' % {'desc': desc, 'dt_string': dt_string}
        run['manage_locator'] = self._run_manage_locator % {'run_name': run['name']}
        run['homepage_locator'] = self._run_homepage_locator % {'run_name': run['name']}
        run['run_tests_locator'] = self._run_tests_button_locator % {'run_name': run['name']}

        self.type(self._name_locator, run['name'])
        self.select(self._cycle_select_locator, cycle)
        self.type(self._description_locator, run['desc'])
        self.type(self._start_date_locator, start_date)
        self.type(self._end_date_locator, end_date)
        if suite:
            self.selenium.add_selection(self._suite_select_locator, suite)
        self.click(self._submit_locator, wait_flag=True)

        return run
