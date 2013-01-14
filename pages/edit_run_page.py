#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base_page import MozTrapBasePage


class MozTrapEditRunPage(MozTrapBasePage):

    _page_title = 'Edit Run'

    _name_locator = (By.ID, 'id_name')
    _product_version_select_locator = (By.ID, 'id_productversion')
    _description_locator = (By.ID, 'id_description')
    _start_date_locator = (By.ID, 'id_start')
    _end_date_locator = (By.ID, 'id_end')
    _series_run_locator = (By.ID, 'id_is_series')
    _include_selected_suites_locator = (By.CSS_SELECTOR, '#run-edit-form .multiselect .include-exclude .action-include')
    _sort_included_suites_by_name_locator = (By.CSS_SELECTOR, '#run-edit-form .multiselected .byname .sortlink')
    _submit_locator = (By.CSS_SELECTOR, '#run-edit-form .form-actions > button')

    def edit_run(self, run, name=None, product_version=None, desc=None,
        start_date=None, end_date=None, reorder_suites=False, series_run=False):

        if name:
            name_field = self.selenium.find_element(*self._name_locator)
            name_field.send_keys(name)
            run['name'] = name

        if product_version:
            product_version_select = Select(self.selenium.find_element(*self._product_version_select_locator))
            product_version_select.select_by_visible_text(product_version)

        if desc:
            self.selenium.find_element(*self._description_locator).send_keys(desc)
            run['desc'] = desc

        if start_date:
            self.type_in_element(self._start_date_locator, start_date)

        if end_date:
            self.type_in_element(self._end_date_locator, end_date)

        if series_run:
            series_element = self.selenium.find_element(*self._series_run_locator)
            if series_element.is_selected():
                if not series_run:
                    series_element.click()
            else:
                if series_run:
                    series_element.click()
            run['series'] = series_run

        if reorder_suites:
            sorter = self.selenium.find_element(*self._sort_included_suites_by_name_locator)
            sorter.click()
            sorter.click()

        self.selenium.find_element(*self._submit_locator).click()

        return run
