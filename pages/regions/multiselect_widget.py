#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import Page, PageRegion


class MultiselectWidget(Page):

    _multiselect_widget_locator = (By.CSS_SELECTOR, '.multiselect')
    _loading_available_items_locator = (By.CSS_SELECTOR, '.multiunselected .select .overlay')
    _loading_included_items_locator = (By.CSS_SELECTOR, '.multiselected .select .overlay')
    _available_item_locator = (By.CSS_SELECTOR, '.multiunselected .selectitem')
    _included_item_locator = (By.CSS_SELECTOR, '.multiselected .selectitem')
    _sort_included_items_by_name_locator = (By.CSS_SELECTOR, '.multiselected .byname .sortlink')
    _include_item_button_locator = (By.CSS_SELECTOR, '.include-exclude .action-include')
    _remove_item_button_locator = (By.CSS_SELECTOR, '.include-exclude .action-exclude')

    @property
    def available_items(self):
        self.wait_for_element_not_present(*self._loading_available_items_locator)
        return [Item(self.testsetup, web_element)
                for web_element in self.find_elements(*self._available_item_locator)]

    @property
    def included_items(self):
        self.wait_for_element_not_present(*self._loading_included_items_locator)
        return [Item(self.testsetup, web_element)
                for web_element in self.find_elements(*self._included_item_locator)]

    def include_items(self, item_names_list):
        # wait till available and included items are loaded
        self.wait_for_element_not_present(*self._loading_available_items_locator)
        self.wait_for_element_not_present(*self._loading_included_items_locator)
        include_button = self.find_element(*self._include_item_button_locator)

        items_to_add = [item
                        for name in reversed(item_names_list)
                        for item in self.available_items
                        if name == item.name]

        for item in items_to_add:
            item.select()
            include_button.click()

    def reorder_included_items(self):
        self.wait_for_element_not_present(*self._loading_included_items_locator)
        sorter = self.find_element(*self._sort_included_items_by_name_locator)
        # requires two clicks to reverse sorting
        sorter.click()
        sorter.click()

    def remove_all_included_items(self):
        self.wait_for_element_not_present(*self._loading_included_items_locator)
        remove_button = self.find_element(*self._remove_item_button_locator)

        for item in self.included_items:
            item.select()

        remove_button.click()

    @property
    def is_present(self):
        return self.is_element_present(*self._multiselect_widget_locator)

    @property
    def is_visible(self):
        return self.is_element_visible(*self._multiselect_widget_locator)


class Item(PageRegion):

    _select_item_locator = (By.CSS_SELECTOR, '.bulk-type')
    _item_title_locator = (By.CSS_SELECTOR, '.title')

    @property
    def name(self):
        return self.find_element(*self._item_title_locator).text

    def select(self):
        self.find_element(*self._select_item_locator).click()
