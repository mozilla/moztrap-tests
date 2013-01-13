#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import MozTrapBasePage


class MozTrapCreateRunPage(MozTrapBasePage):

    _page_title = 'Create Run'

    _name_locator = (By.ID, 'id_name')
    _product_version_select_locator = (By.ID, 'id_productversion')
    _description_locator = (By.ID, 'id_description')
    _start_date_locator = (By.ID, 'id_start')
    _end_date_locator = (By.ID, 'id_end')
    _suite_select_locator = (By.CSS_SELECTOR, '#run-add-form .multiunselected .itemlist article.selectitem[data-title="%(suite_name)s"] input.bulk-value')
    _include_selected_suites_locator = (By.CSS_SELECTOR, '#run-add-form .multiselect .include-exclude .action-include')
    _submit_locator = (By.CSS_SELECTOR, '#run-add-form .form-actions > button')
    _run_manage_locator = (By.CSS_SELECTOR, '#manageruns .itemlist .listitem .title[title="%(run_name)s"]')
    _run_homepage_locator = (By.CSS_SELECTOR, '.runsdrill .runsfinder .runs .colcontent .title[title="%(run_name)s"]')
    _run_tests_button_locator = (By.CSS_SELECTOR, 'div.form-actions > button')
    _series_run_locator = (By.ID, 'id_is_series')

    def go_to_create_run_page(self):
        self.selenium.get(self.base_url + '/manage/run/add/')
        self.is_the_current_page

    def create_run(self, name='Test Run', product_version='Test Product Test Version', desc='This is a test run', start_date='2011-01-01', end_date='2012-12-31', suite_list=None, series_run=False):
        dt_string = datetime.utcnow().isoformat()
        run = {}
        run['name'] = u'%(name)s %(dt_string)s' % {'name': name, 'dt_string': dt_string}
        run['desc'] = u'%(desc)s created on %(dt_string)s' % {'desc': desc, 'dt_string': dt_string}
        run['series'] = series_run
        run['manage_locator'] = (self._run_manage_locator[0], self._run_manage_locator[1] % {'run_name': run['name']})
        run['homepage_locator'] = (self._run_homepage_locator[0], self._run_homepage_locator[1] % {'run_name': run['name']})
        run['run_tests_locator'] = self._run_tests_button_locator

        name_field = self.selenium.find_element(*self._name_locator)
        name_field.send_keys(run['name'])

        series_element = self.selenium.find_element(*self._series_run_locator)

        if series_element.is_selected():
            if not series_run:
                series_element.click()
        else:
            if series_run:
                series_element.click()

        product_version_select = Select(self.selenium.find_element(*self._product_version_select_locator))
        product_version_select.select_by_visible_text(product_version)

        self.selenium.find_element(*self._description_locator).send_keys(run['desc'])

        self.type_in_element(self._start_date_locator, start_date)
        self.selenium.find_element(*self._end_date_locator).send_keys(end_date)

        if suite_list:

            for suite in suite_list:
                suite_input_element = self.selenium.find_element(By.XPATH, "//article[@data-title='%s']//label" % suite)
                suite_input_element.click()
            self.selenium.find_element(*self._include_selected_suites_locator).click()
        self.selenium.find_element(*self._submit_locator).click()

        return run

    @property
    def product_version(self):
        product_version_select = Select(self.selenium.find_element(*self._product_version_select_locator))
        return product_version_select.first_selected_option.text
