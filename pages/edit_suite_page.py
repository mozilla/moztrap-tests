# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base_page import MozTrapBasePage
from pages.regions.multiselect_widget import MultiselectWidget


class MozTrapEditSuitePage(MozTrapBasePage):

    _page_title = 'Edit Suite'

    _product_field_locator = (By.CSS_SELECTOR, '.formfield.product-field .value')
    _save_suite_button_locator = (By.CSS_SELECTOR, '#suite-edit-form .form-actions > button')

    @property
    def is_product_field_readonly(self):
        product_field = self.find_element(*self._product_field_locator)
        if product_field.tag_name == u'select' and product_field.is_enabled():
            return False
        else:
            return True

    def save_suite(self):
        self.find_element(*self._save_suite_button_locator).click()

    @property
    def multiselect_widget(self):
        return MultiselectWidget(self.testsetup)

    def include_cases_to_suite(self, case_list, save_suite=True):
        self.multiselect_widget.include_items(case_list)
        if save_suite:
            self.save_suite()

    @property
    def included_cases(self):
        return self.multiselect_widget.included_items

    @property
    def available_cases(self):
        return self.multiselect_widget.available_items

    def remove_all_included_cases(self):
        self.multiselect_widget.remove_all_included_items()
