#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.base_page import MozTrapBasePage
from datetime import datetime


class MozTrapCreateRunPage(MozTrapBasePage):

    _page_title = 'MozTrap'

    _name_locator = 'id=id_name'
    _product_version_select_locator = 'id=id_productversion'
    _description_locator = 'id=id_description'
    _start_date_locator = 'id=id_start'
    _end_date_locator = 'id=id_end'
    _suite_select_locator = u'css=#run-add-form .multiunselected .itemlist article.selectitem[data-title="%(suite_name)s"] input.bulk-value'
    _include_selected_suites_locator = 'css=#run-add-form .multiselect .include-exclude .action-include'
    _submit_locator = 'css=#run-add-form .form-actions > button'
    _run_manage_locator = u'css=#manageruns .itemlist .listitem .title[title="%(run_name)s"]'
    _run_homepage_locator = u'css=.runsdrill .runsfinder .runs .colcontent .title[title="%(run_name)s"]'
    _run_tests_button_locator = u'css=#runtests-environment-form .form-actions button:contains(run tests in %(run_name)s!)'

    def go_to_create_run_page(self):
        self.selenium.open('/manage/run/add/')
        self.is_the_current_page

    def create_run(self, name='Test Run', product_version='Test Product Test Version', desc='This is a test run', start_date='2011-01-01', end_date='2012-12-31', suite_list=None):
        dt_string = datetime.utcnow().isoformat()
        run = {}
        run['name'] = u'%(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
        run['desc'] = u'%(desc)s created on %(dt_string)s' % {'desc': desc, 'dt_string': dt_string}
        run['manage_locator'] = self._run_manage_locator % {'run_name': run['name']}
        run['homepage_locator'] = self._run_homepage_locator % {'run_name': run['name']}
        run['run_tests_locator'] = self._run_tests_button_locator % {'run_name': run['name']}

        self.type(self._name_locator, run['name'])
        self.select(self._product_version_select_locator, product_version)
        self.type(self._description_locator, run['desc'])
        self.type(self._start_date_locator, start_date)
        self.type(self._end_date_locator, end_date)
        if suite_list:
            for suite in suite_list:
                _suite_select_locator = self._suite_select_locator % {'suite_name': suite}
                self.selenium.check(_suite_select_locator)
            self.click(self._include_selected_suites_locator)
        self.click(self._submit_locator, wait_flag=True)

        return run
